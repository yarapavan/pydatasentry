#!/usr/bin/env python

import json 
import pickle 
from .helpers import dumper
from .lineage import get_lineage

#{
#    "spec": {
#        "storage": [
#            "local"
#        ],
#        "experiment": {
#            "scope": "test",
#            "version": 1,
#            "run": "test"
#        },
#        "output": [
#            "output.default-signature"
#        ],
#        "instrumentation": {
#            "modules": [
#                "statsmodels.formula.api"
#            ]
#        }
#    },
#    "attributes": {
#        "dataset.id": {
#            "compute": "<function <lambda> at 0x7fd373569268>"
#        },
#        "model.common.timestamp": {
#            "compute": "<function <lambda> at 0x7fd373569510>"
#        },
#        "dataset.transformations": {
#            "compute": "<function <lambda> at 0x7fd373569400>"
#        },
#        "output.default-signature": {
#            "compute": "<function compute_default_signature at 0x7fd3735691e0>",
#            "params": {
#                "format": "JSON"
#            },
#            "inputs": {
#                "modeling-function": "model.function",
#                "columns": "model.data.columns",
#                "uuid": "uuid",
#                "modeling-module": "model.module",
#                "data-dimensions": "model.data.shape"
#            }
#        },
#        "model.data.shape": {
#            "compute": "<function <lambda> at 0x7fd373569598>",
#            "inputs": {
#                "dataset": "model-parameters.data"
#            }
#        },
#        "dataset.relativepath": {
#            "compute": "<function dataset_relpath at 0x7fd3735690d0>"
#        },
#        "model.modname": {
#            "compute": "<function <lambda> at 0x7fd373569488>"
#        },
#        "storage.local": {
#            "store": "<function local_storage at 0x7fd373569158>",
#            "params": {
#                "relative-path": [
#                    "model-output",
#                    "spec.scope",
#                    "spec.run",
#                    "spec.version",
#                    "model.common.timestamp",
#                    "model.common.formula"
#                ]
#            }
#        },
#        "dataset.hash": {
#            "compute": "<function <lambda> at 0x7fd3735692f0>"
#        },
#        "dataset.name": {
#            "compute": "<function dataset_basename at 0x7fd373564f28>"
#        },
#        "dataset.timestamp": {
#            "compute": "<function <lambda> at 0x7fd373569378>"
#        },
#        "model.data.columns": {
#            "compute": "<function <lambda> at 0x7fd373569620>",
#            "inputs": {
#                "dataset": "model-parameters.data"
#            }
#        }
#    },
#    "datasets": [],
#    "debug": true
#}
#

def lookup_attribute(name, run): 
    """
    Looks up the run configuration for the value of a given
    attribute. The function tries a couple of options before giving
    up. The default is to return the name unmodified
    
    :param name: name of the attribute
    :param run: Combination of configuration and run-specific  information (internally generated)
    :returns attribute: dict corresponding to the attribute

    """
    print("Default lookup", name) 

    # See if a simple lookup will work..
    if name in run: # model
        print("Default lookup. Basic", name, run[name])
        return run[name] 

    # May be the name is nested. So try that as well..
    try:
        # Try run['model']['function']
        alt = "['" + name.replace(".","']['") + "']"
        alt = "run"+alt
        res = eval(alt)
        print("Default lookup. Bracketed", alt, res)
        return res  
    except Exception as e:
        print("Default lookup. Bracketed", alt, "Didnt work")
        pass 
        
    # Nothing worked. Simply return the name 
    print("Default lookup. Nothing worked", name) 
    return name 

def evaluate_attribute(name, run, form=str, depth=0): 
    """
    Evaluate the signature and other attributes specified by the
    configuration. 
    
    :param name: Name of the attribute
    :param run: Combination of configuration and run-specific  information (internally generated)
    :param depth: <internal parameter to track recursion> 
    """
    # Evaluate pre-requisites 
    debug = run.get('debug', False) 

    if debug: 
        print("Evaluate ", name, "Depth", depth)
    
    if isinstance(name, dict): 
        result = {} 
        for e in name: 
            result[e] = evaluate_attribute(name[e],
                                           run,
                                           form, 
                                           depth+1)
        return result 

    if isinstance(name, list): 
        result = []
        for e in name: 
            result.append(evaluate_attribute(e,
                                             run,
                                             form, 
                                             depth+1))
        return result 


    # The result may be a simple string...
    attribute = lookup_attribute(name, run)        
    
    # We may not have found any attribute to process. So simply return
    # the same..
    if ((not isinstance(attribute, dict)) or
        (('params' not in attribute) and 
         ('compute' not in attribute))):
        print("Attribute name", name, 
              "not found or the data does not "
              "look like an attribute.",
              "So returning the attribute", attribute)
        return attribute

    # Now the 
    params = attribute.get('params', {})
    
    # Turn params into args 
    args = evaluate_attribute(params, run) 
    
    # Gather the computation...
    compute = attribute.get('compute', 
                            lambda run, args: args)
            
    print("Found ", json.dumps(args, default=dumper, indent=4))
    print("Calling compute of ", name)
    return compute(run, args) 


def summarize_run(run): 
    """
    Post-process the input and output data from the run. 

    :param run: Combination of configuration and run-specific  information (internally generated)

    """
    if run['debug']: 
        print("Document")
        print(json.dumps(run, default=dumper, indent=4))
    

    # Gather what should be computed...
    evaluate_attribute("spec.store", run)

