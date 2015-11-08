#!/usr/bin/env python 

import uuid 
import inspect 
import json
import os, sys 
import copy 
from .config import get_config
from .helpers import dumper, merge
from .process import summarize_run

def capture_input(args, kwargs, metadata): 
    """
    Capture the function parameters for the functions that have been instrumented
    """
    formula = kwargs.get('formula', None)
    data = kwargs.get('data', None) 
    sentryopts = kwargs.pop('sentryopts', {})

    # Inspect and get the source files...
    curframe = inspect.currentframe()
    calframes = inspect.getouterframes(curframe, 3)
    filename = os.path.realpath(calframes[2][1])
    lineno = calframes[2][2] 
    snippet = calframes[2][4] 
    uid = str(uuid.uuid1())

    params = {
        'uuid': uid, 
        'source': {
            'filename': filename, 
            'lineno': lineno,
            'snippet': snippet
        },  
        'model': {
            'library': { 
                'module': metadata['modname'],
                'function': metadata['funcname']
            },            
            'parameters': {
                'formula': formula, 
                'data': data
            },        
        }
        #'other parameters': {
        #    'args': args, 
        #    'kwargs': kwargs 
        #},
    }

    run = get_config()    
    merge(run, params)
    merge(run, sentryopts) 

    return run 
    
def capture_output(run, result): 
    """
    Capture the results of the instrumented function
    """
    run['model']['result'] = result
    summarize_run(run)
    return 

    
