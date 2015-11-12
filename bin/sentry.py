#!/usr/bin/env python 

"""
sentry.py allows instrumenting a python/pandas program with no
modifications to the program itself. Note that only python 3 is supported. 

::

   sentry.py help 
   sentry.py init <sentry-conf.py>
   sentry.py example <filename.py>
   sentry.py [run|commit] [-c <sentry-conf.py>] <python-program-to-be-instrumented>"

   run and commit are almost the same. The latter suggest final
   run. Only committed runs are stored/uploaded. 

"""

import pydatasentry 
import os, sys 
import imp
import shutil 
from importlib.machinery import SourceFileLoader

def load_program():
    """
    Load the user's command line
    """
    path = sys.argv[1] 
    with open(path) as f:
        code = compile(f.read(), path, 'exec')
        ldict = locals()
        exec(code, globals(), ldict)

def load_configuration(conf): 

    if conf is None: 
        return {} 

    conf = os.path.abspath(conf) 

    if not os.path.exists(conf): 
        print("Configuration file not present:", conf) 
        sys.exit()

    print("Configuration path", conf) 

    mod = SourceFileLoader("module.name", conf).load_module()    
    return mod.get_config() 

def sentry_help():
    print("sentry: Transparently instrument pandas code") 
    print("sentry.py help")
    print('sentry.py init <sentry-conf.py>')
    print('sentry.py example <basic_ols.py>')
    print('sentry.py run [-c|--config <sentry-conf.py>]  <python-program-to-be-instrumented>')

def initialize(conf): 
    """
    Initialize a sentry configuration file 
    
    :param conf: sentry configuration file 
    """

    if os.path.exists(conf): 
        print("File already exists. Please remove first:", conf) 
        sys.exit() 

    rootdir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
    template = os.path.realpath(os.path.join(rootdir, 
                                             "share",
                                             "sentry-conf.py.template"))
    shutil.copyfile(template, conf) 
    print("Updated", conf)

def example(path): 
    """
    Initialize a sentry configuration file 
    
    :param conf: sentry configuration file 
    """

    if os.path.exists(path): 
        print("File already exists. Please remove first:", path) 
        sys.exit() 

    rootdir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
    template = os.path.realpath(os.path.join(rootdir, 
                                             "share",
                                             "basic_ols.py.template"))
    shutil.copyfile(template, path) 
    print("Updated", path)
    
def main():
    
    offset = 1
    conf=None

    # Check for help...
    if len(sys.argv) == 1 or sys.argv[1] in ["help"]:
        sentry_help()
        sys.exit()

    
    cmd = sys.argv[0]
    sys.argv = sys.argv[1:]
    if sys.argv[0] in ["init"]: 
        if len(sys.argv) < 2: 
            print("Missing filename argument") 
            sentry_help()
            sys.exit() 
        initialize(conf=sys.argv[1])
        sys.exit() 

    if sys.argv[0] in ["example"]: 
        if len(sys.argv) < 2: 
            print("Missing filename argument") 
            sentry_help()
            sys.exit() 
        example(path=sys.argv[1])

    if sys.argv[0] in ["run", "commit"]: 
        runcmd = sys.argv[0]

        if len(sys.argv) < 2: 
            print("Missing arguments") 
            sentry_help()
            sys.exit() 

        # Handle the configuration option...
        sys.argv = sys.argv[1:]
        print("Before config", sys.argv) 
        if sys.argv[0] in ["-c", "--conf"]:
            if len(sys.argv) < 3: 
                print("Missing configuration file") 
                sentry_help()
                sys.exit() 

            conf = sys.argv[1] 
            config = load_configuration(conf)             
            sys.argv = sys.argv[2:]
        else: 
            config = {} 
        
        if 'spec' not in config: 
            config['spec'] = {} 
        config['spec']['run'] = runcmd 

        if sys.argv[0] in ["-m", "--message"]:
            if len(sys.argv) < 3: 
                print("Missing configuration file") 
                sentry_help()
                sys.exit() 
            message = sys.argv[1] 
            config['spec']['message'] = message
            sys.argv = sys.argv[2:]

        print("Found config", config) 
        pydatasentry.initialize(config) 

        # Now load the program...
        sys.argv.insert(0, cmd) 
        load_program()

if __name__ == "__main__":
    main()
