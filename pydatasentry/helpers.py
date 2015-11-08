#!/usr/bin/env python 

import os, sys 
import hashlib 
from datetime import datetime
import json


def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        # print("Looking at ", key)
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            elif type(a[key]) == type(b[key]): 
                a[key] = b[key]
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            # print("Adding new key", key) 
            a[key] = b[key]
    return a

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        try:
            return str(obj)
        except: 
            return obj.__dict__


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

def dataset_basename(datasetname): 
    return os.path.basename(config.config['datasets'][dataset]['filename'])


def dump_signature(run): 

    signature = compute_signature(run)

    for backend in run['storage']['backends']: 
        path = run['storage']['backends'][backend]['compute'](run)
        
        content = json.dumps(signature, indent=4)
        run['storage']['backends'][backend]['store'](run, 
                                                     path, 
                                                     'signature.json',
                                                     content) 

def dataset_relpath(datasetname): 
    
    # Get the most specific path that you can get to ...
    rootdir = config.config['datasets'][dataset].get('rootdir', None)
    if rootdir is None: 
        rootdir = config.config['datasets'].get('rootdir', None)
    if rootdir is None: 
        rootdir = getcwd()

    relpath = os.path.relpath(config.config['datasets'][dataset]['filename'], rootdir)
    return relpath 

def local_storage_helper(path, filename, content):         
    
    print("local_storage_helper", path, filename, type(content))

    # Make sure that output dir exists..
    try:
        os.makedirs(path)
    except: 
        pass 

    path = os.path.join(path, filename)
    if os.path.exists(path): 
        print("Overwriting existing file")
        raise Exception("Output clobber") 

    if isinstance(content, str): 
        fd = open(path, 'w')
    else: 
        fd = open(path, 'wb')
    fd.write(content)
    fd.close()
        
    print("Wrote to ", path)

def local_storage(run, args): 
    print("local storage") 

    # Get the output list
    for o in args['output']:
        path = [str(x) for x in o['path']]
        path = os.path.join(*path)
        filename = o['filename']        
        content = o['content'] 
        local_storage_helper(path, filename, content)
    
    return "None" 

def compute_default_signature(run, params): 
    
    print("Computing params", params) 
    return 

