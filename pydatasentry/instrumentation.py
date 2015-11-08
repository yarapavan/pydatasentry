#!/usr/bin/env python
"""
This is the instrumentation library. It instruments all the functions
in the modules specified in the spec (see config)
"""
import importlib
import types 
import json
from .capture import capture_input, capture_output 
from .config import get_config

intercepted_functions = []

def cleanup_instrumentation(): 
    """
    Remove the interception for all functions. 
    """
    global intercepted_functions

    for r in intercepted_functions: 
        modname  = r['modname']
        mod      = r['mod']
        funcname = r['funcname']
        orig_func= r['original']
        vars(mod)[funcname] = orig_func

def intercept(func, metadata):
    """
    Helper wrapper function that captures the input and output to
    every instrumented function
    """
    def with_intercept(*args, **kwargs):
        run = capture_input(args, kwargs, metadata) 
        output = func(*args, **kwargs)
        capture_output(run, output) 
        return output

    return with_intercept
    
def instrument(): 
    """
    Instrument each of the modules specified in the config['spec']['instrumentation']['modules']
    """
    config = get_config() 
    modules = config['spec']['instrumentation']['modules']
    if config['debug']: 
        print("Instrumenting", modules)
    for m in modules: 
        mod = importlib.import_module(m)
        for k,v in vars(mod).items():
            if isinstance(v, types.MethodType):
                intercepted_functions.append({
                    'modname': m, 
                    'mod': mod,
                    'funcname': k,
                    'original': v,
                })
                metadata = intercepted_functions[-1]
                wrapper_func = intercept(v, metadata)
                metadata['wrapper'] = wrapper_func 
                vars(mod)[k] = wrapper_func
    
