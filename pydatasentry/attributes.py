#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""

These are the set of attributes that can be computed for each run. The
configuration specifies which subset of these should be stored, how
and where. 

The attributes provide a fairly expressive language to collect
information recursively. Each attribute can combine multiple other
attributes' values to generate new values 

The default module that is instrumented is statsmodels.formula.api
and the storage is local. 

"""

import os, sys 
import hashlib 
from datetime import datetime
from json import JSONEncoder
from .helpers import * 
import pickle 

attribute_overlay = { 

    'model': {
        'parameters': {
            'datashape': {
                'params': {
                    'dataset': 'model.parameters.data'
                },        
                'compute': lambda run, args: args['dataset'].shape
            },
            'datacolumns': {
                'params': {
                    'dataset': 'model.parameters.data'
                },        
                'compute': lambda run, args: list(args['dataset'].columns)
            },
        },
    },

    'attributes': { 
        'generic': {
            'timestamp': {
                'compute': lambda run, args : datetime.now().strftime("%Y-%b-%d-%H:%M:%S")
            },
        },
        'output': { 
            'relative-path': {
                'params': [
                    'model-output',
                    'spec.experiment.scope', 
                    'spec.experiment.run', 
                    'spec.experiment.version', 
                    'model.library.function',
                    'uuid', 
                    'attributes.generic.timestamp'
                ],
                'compute': lambda run, args: os.path.join(args)
            },
            'default-signature': {
                'params': {
                    'uuid': 'uuid',
                    'experiment': {
                        'scope': 'spec.experiment.scope',
                        'run': 'spec.experiment.run',
                        'version': 'spec.experiment.version'
                    },
                    'data': {
                        'name': 'dataset',
                        'shape': 'model.parameters.datashape',
                        'columns': 'model.parameters.datacolumns'
                        },
                    'model': { 
                        'module': 'model.library.module',
                        'function': 'model.library.function',
                        'formula': 'model.parameters.formula'

                    }
                },
                'compute': lambda run, args: json.dumps(args, indent=4)
            },
            'full-pickle': {
                'params': {
                    'result': 'model.result'
                },
                'compute': lambda run, args: pickle.dumps(args['result'].fit())
            },
            'summary-pickle': {
                'params': {
                    'result': 'model.result'
                },
                'compute': lambda run, args: pickle.dumps(args['result'].fit().summary())
            },
        },
        'storage': {
            'local': { 
                'params': {
                    'output': 'spec.output',
                },
                'compute': lambda run, args: local_storage(run, args)
            }
        }
    } 
}

