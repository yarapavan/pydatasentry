PyDataSentry - Memory for Data Science
======================================

pydatasentry package allows auditability of modeling code and data by
logging all relevant information for every single model run (e.g., a
regression)

Background
~~~~~~~~~~

Audience

Mainly data scientists that run statistical models using
pandas/statsmodels/scikit-learn of various kinds on a regular basis.

Problem

The combination of datasets, questions, and nature of analysis is
growing everyday. Data scientists find it hard to keep track of all
the different datasets they dealt with, what they did with those
datasets, and what they presented to the model-audience (business etc)

Solution

pydatasentry package allows auditability of modeling code and data by
logging all relevant information for every single model run (e.g., a
regression) You could use this for audit past results for correctness,
share models and results with peers, search past results to avoid
repition of work.

Features 
~~~~~~~~

* Automatic interception of the library calls. Right now only
  statsmodels.formula.api is supported. But the support can be easily
  extended to other libraries

* Capture of all relevant context for each run including the signature
  (who called, with what parameters etc.), the input dataset, the
  resulting object (full and summary versions). In addition parameters
  (sentryopt) can be passed to the library call that is extracted and
  captured (e.g., a set of tags)

* Storage in local directory in systematic way locally and remotely if
  needed.


* Optional github commit information to know what code was responsible
  for this call.

And all these can be over-ridden and extended. 

Installation
~~~~~~~~~~~~

::

    git clone git@github.com:FourthLion/pydatasentry.git
    cd pydatasentry 
    python setup.py install

Examples 
~~~~~~~~~

Minimal: 

Only two lines are required by default. Please check the config module
to know what are the defaults for what needs to be captured
(dataframes, statsmodels interface, signature) and where they should
be stored (local directory 'model-output')

::

    #!/usr/bin/env python
    
    import os, sys 
    import pandas as pd
    import statsmodels.formula.api as smf
    import pydatasentry 
    
    if __name__ == "__main__": 

        pydatasentry.initialize()
        
        df = pd.DataFrame({"A": [10,20,30,40,50], 
                               "B": [20, 30, 10, 40, 50], 
                               "C": [32, 234, 23, 23, 42523]})
        
        result = smf.ols(formula="A ~ B + C", 
                         data=df
                     ).fit()
    
        print(result.summary())

The output is stored in a experiment and time dependent directory that
has a unique identifier associated with it.

::

    $ find model-output
    model-output
    model-output/offers
    model-output/offers/conditional
    model-output/offers/conditional/1
    model-output/offers/conditional/1/ols
    model-output/offers/conditional/1/ols/96f5b468-85ee-11e5-b3b5-0800274d1e8c
    model-output/offers/conditional/1/ols/96f5b468-85ee-11e5-b3b5-0800274d1e8c/2015-Nov-08-13:29:08
    model-output/offers/conditional/1/ols/96f5b468-85ee-11e5-b3b5-0800274d1e8c/2015-Nov-08-13:29:08/full.pickle
    model-output/offers/conditional/1/ols/96f5b468-85ee-11e5-b3b5-0800274d1e8c/2015-Nov-08-13:29:08/signature.json
    model-output/offers/conditional/1/ols/96f5b468-85ee-11e5-b3b5-0800274d1e8c/2015-Nov-08-13:29:08/summary.pickle
    
    $ cat model-output/offers/conditional/1/ols/96f5b468-85ee-11e5-b3b5-0800274d1e8c/2015-Nov-08-13:29:08/signature.json
    {
        "data": {
            "name": "random",
            "columns": [
                "A",
                "B",
                "C"
            ],
            "shape": [
                5,
                3
            ]
        },
        "uuid": "51ef2ae4-85ed-11e5-a8bc-0800274d1e8c",
        "model": {
            "module": "statsmodels.formula.api",
            "formula": "A ~ B + C",
            "function": "ols"
        },
        "experiment": {
            "scope": "test",
            "version": 1,
            "run": "test"
        }
    }
    
    
Detailed:

pydatasentry gives the user control over every aspect of the process.
The example below shows the user over-riding the experiment details, 
output parameters, and tracking lineage. 

::

    #!/usr/bin/env python
    
    import os, sys 
    import pandas as pd
    import statsmodels.formula.api as smf
    import pydatasentry 
    
    if __name__ == "__main__": 

        # Specify what and how of the capture in great detail
        pydatasentry.initialize({
            'debug': True, 
            
            'spec': { 
                'experiment': { 
                    'scope': 'test',
                    'run': 'test',
                    'version': 1
                },
                'output': {
                    'params': [ 
                        {
                            'content': 'attributes.output.default-signature',
                            'path': 'attributes.output.relative-path',
                            'filename': 'signature.json'
                        }
                    ]
                },
            },
        }) 
        
    with tracklineage("load", "sample"): 
        df = pd.DataFrame({"A": [10,20,30,40,50], 
                               "B": [20, 30, 10, 40, 50], 
                               "C": [32, 234, 23, 23, 42523]})
        
        result = smf.ols(formula="A ~ B + C", 
                         data=df, 
                         sentryopts={
                             'dataset': "sample"
                         }
                     ).fit()
    
        print(result.summary())

Next Steps
~~~~~~~~~~

This is just a starting point. We intend to extend the pydatasentry to
cover other modeling libraries, and capture dependencies. Please let
me (pingali@gmail.com) know or post an issue

License
~~~~~~~

Standard MIT License. See LICENSE.txt 

Acknowledgements
~~~~~~~~~~~~~~~~

To FourthLion for agreeing to contribute this code back to the
community. 
