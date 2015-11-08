#!/usr/bin/env python 
"""
"""
import os, sys 
import pandas as pd 
import libsettings 
from datetime import datetime 
import glob2 
import json
import pickle 

def update_dataset_signature():
    """
    Compute the signature only once...
    """

    signature_definition = libsettings.config['signature']['definition']
    config = libsettings.config 
    signature = {}
    for name, instruction in signature_definition.items(): 
        compute = instruction.get('compute', 
                                  lambda config: None)
        result = compute(config)
        signature[name] = result 

    libsettings.config['dataset-signature'] = signature 


def compute_signature(formula):
    
    if 'dataset-signature' not in libsettings.config: 
        update_dataset_signature()

    signature = {
        'formula': formula,
        'dataset': libsettings.config['dataset-signature']
    }

    return signature 
    
def check_if_exists(name, what, formula, mod): 
    
    signature = compute_signature(formula) 

    outputdir = libsettings.config['outputdir']
    filename= formula.replace(" ","-") 
    signatures = glob2.glob(os.path.join(outputdir, 
                                         "**",
                                         name,
                                         "**",
                                         "signature.json"
                                     ))

def store_regression_result(name, what, formula, mod, overwrite): 
    
    print("Store result", formula) 

    now = datetime.now()
    ts = now.strftime("%Y-%b-%d") 
    formula_filename = formula.replace(" ", "-")
    outputdir = os.path.join(libsettings.config['outputdir'],
                             ts, 
                             what,
                             formula_filename)
    try: 
        os.makedirs(outputdir)
    except:
        pass 
        
    
    # Compute and store the signature 
    signature = compute_signature(formula)     
    path = os.path.join(outputdir, 'signature.json')
    if not overwrite and os.path.exists(path): 
        print("Signature file", path, "already exists")
        raise Exception("Clobber")
    fd = open(path,'w')
    fd.write(json.dumps(signature, indent=4))
    fd.close() 

    # Dump the regression file...
    path = os.path.join(outputdir, 'regression-full.pickle')
    if not overwrite and os.path.exists(path): 
        print("Pickle file", path, "already exists")
        raise Exception("Clobber")
    fd = open(path,'wb')
    pickle.dump(mod, fd)
    fd.close() 


    # Dump the regression file...
    path = os.path.join(outputdir, 'regression-summary.pickle')
    if not overwrite and os.path.exists(path): 
        print("Pickle file", path, "already exists")
        raise Exception("Clobber")
    fd = open(path,'wb')
    pickle.dump(mod.summary(), fd)
    fd.close() 

    
                             
