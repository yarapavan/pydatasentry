#!/usr/bin/env python
"""
pydatasentry package allows auditability of modeling
code and data by logging all relevant information for every single
model run (e.g., a regression) 

"""
from .instrumentation import * 
from .config import initialize_config, validate_config
from .helpers import dumper 

def initialize(revised_config={}):
    
    # Load up the config 
    initialize_config(revised_config) 
    validate_config() 
    instrument() 
    
