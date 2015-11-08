#!/usr/bin/env python 
"""

Maintains the overall configuration. Any over-rides provided by the
users are incorporated into the configuration. The configuration is
combined with run-specific data to the post-processing function. 

The default configuration is 
:: 
     {
        'debug': False, 
        'spec': {         

            # High level experiment information
            'experiment': { 
                'scope': 'offers',
                'run': 'conditional-offers',
                'version': 1
            },

            # Which modules should be instrumented 
            'instrumentation': {
                'modules': ['statsmodels.formula.api']
            },

            # What should be captured 
            'output': {
                'params': [ 
                    {
                        'content': 'attributes.output.default-signature',
                        'path': 'attributes.output.relative-path',
                        'filename': 'signature.json'
                    }
                ]
            },

            # Where should they be stored and how 
            'store': {
                'params': ['attributes.storage.local']
            },

     }

"""
import os, sys  
import copy 
import json
from .helpers import dumper, merge
from .attributes import attribute_overlay

def initialize_config(update={}): 
    """
    Initialize the configuration of pydatasentry and over-ride it with
    with any user or run specific parameters

    :param update: Dict that over-rides the basic configuration
    """
    global config 
    config = {
        'debug': False, 
        'spec': {         
            # High level experiment information
            'experiment': { 
                'scope': 'offers',
                'run': 'conditional',
                'version': 1
            },
            # Which modules should be instrumented 
            'instrumentation': {
                'modules': ['statsmodels.formula.api']
            },
            # What should be captured and where
            'output': {
                'params': [ 
                    {
                        'content': 'attributes.output.default-signature',
                        'path': 'attributes.output.relative-path',
                        'filename': 'signature.json',
                        'format': 'JSON'
                    },
                    {
                        'content': 'attributes.output.full-pickle',
                        'path': 'attributes.output.relative-path',
                        'filename': 'full.pickle',
                        'format': 'JSON'
                    },
                    {
                        'content': 'attributes.output.summary-pickle',
                        'path': 'attributes.output.relative-path',
                        'filename': 'summary.pickle',
                        'format': 'JSON'
                    },
                    
                ]
            },
            # Storage engine
            'store': {
                'params': ['attributes.storage.local']
            },
            
        } # spec
    }
    
    # Include the attribute map...
    merge(config, attribute_overlay)

    # Override the helper functions and spec if needed...    
    merge(config, update)
    
    #if config['debug']:
    #    print("Post initialization")
    #    print(json.dumps(config, default=dumper, indent=4))

def get_config(): 
    """
    Read the configuration 

    :returns: current configuration

    """
    global config 
    return copy.deepcopy(config)

def validate_config():    
    """
    Checks whether the specified configuration has all the essential
    fields such as the experiment details. More checks will be added
    over time. 
    
    :returns: "Invalid configuration" exception if there is an issue
    """
    global config

    #if config['debug']: 
    #    print("config: [Validate Config]")
    #    print(json.dumps(config, default=dumper, indent=4))

    if 'experiment' not in config['spec']: 
        print("pydatasentry requires specification of " \
              "'experiment'. Please check documentation", file=sys.stderr) 
        raise Exception("Invalid configuration")

    required = ['scope', 'run', 'version']
    missing = [r for r in required if r not in config['spec']['experiment']]
    if len(missing) > 0: 
        print("pydatasentry requires atleast modeling scope (e.g., " \
              "offers), run (e.g., regional model), and version (e.g., \
              v1", file=sys.stderr) 
        raise Exception("Invalid configuration")

