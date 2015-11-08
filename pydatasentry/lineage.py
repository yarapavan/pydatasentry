#!/usr/bin/env 
"""

Track lineage of any dataset from the point it is loaded and pass it
in the signature. 

"""
import uuid 
from contextlib import ContextDecorator
import json
from .config import get_config 

lineage = {}
"""
Maintain a experiment-specific lineage
"""

datasets = {} 
"""
Maintain a experiment-specific list of datasets
"""

class track(ContextDecorator):
    """

    Track lineage of each dataset - load, transform, and store. This
    is provided as a "With" decorator. We expect this to be automatic
    in future. 
    
    """
    def __init__(self, action, notes="", **kwargs): 
        """
        
        :param action: Supported actions include load, store, transform 
        :param notes: Any human readable description (could be empty)
        :param source: Required for load (usually a filename) 
        :param inputdatasets: Required for transform and store actions (list)
        :param outputdatasets: Required for load and transform actions (list)
        """

        global lineage, datasets 

        # Construct a new lineage entry...
        entry = {
            'action': action,
            'notes': notes,
        }
        entry.update(kwargs)
        sanity_check(entry)
        update_datasets(entry)
        
        # Update the lineage for a given experiment...
        experiment = get_config()['spec']['experiment']
        context = "%(scope)s" % experiment    
        if context not in lineage: 
            lineage[context] = []
        lineage[context].append(entry) 


    def __enter__(self):
        # May add new checks/logs later
        return self
    
    def __exit__(self, *exc):
        # May add new checks/logs later
        return False

def update_datasets(entry): 
    """

    """
    global datasets 
    
    experiment = get_config()['spec']['experiment']
    context = "%(scope)s" % experiment    
    if context not in datasets: 
        datasets[context] = {} 

    if entry['action'] == "load": 
        dflist = entry['outputdatasets']
        for df in dflist: 
            if df not in datasets[context]: 
                datasets[context][df] = {
                    'how': 'user-specified',
                    'source': entry.get('source', 'Unknown'),
                    'errors': []
                }
            else: 
                datasets[context][df]['errors'].append("Multiple entry")
                print("WARNING: dataset ", df, 
                      "already loaded",file=sys.stderr) 

    elif entry['action'] == "transform": 
        dflist = entry['inputdatasets']
        for df in dflist: 
            if df not in datasets[context]: 
                datasets[context][df] = {
                    'source': entry.get('source', 'Unknown'),
                    'errors': ['created by default']
                }
        
        dflist = entry['outputdatasets']
        for df in dflist: 
            if df not in datasets[context]: 
                datasets[context][df] = {
                    'source': 'transformation'
                }

    elif entry['action'] == "store": 
        dflist = entry['inputdatasets']
        for df in dflist: 
            if df not in datasets[context]: 
                datasets[context][df] = {
                    'source': 'unknown',
                    'errors': ['created by default']
                }

def sanity_check(entry): 
    """

    Sanity check the lineage annotation for the required parameters

    """
    global datasets 

    supported_args = {
        'load' : ['source'],
        'transform': ['inputdatasets', 'outputdatasets'],
        'store': ['inputdatasets']
    }

    action = entry['action']
    if action not in supported_args: 
        print("Invalid action specified with tracklineage")
        raise Exception("Invalid action")
        
    missing = [arg for arg in supported_args[action] if arg not in entry]
    if len(missing) > 0: 
        print("Expected arguments for ",action,":",",".join(supported_args[action]))
        raise Exception("Invalid parameters")


def get_lineage():
    """
    :returns lineage: history until now
    """
    return lineage 




