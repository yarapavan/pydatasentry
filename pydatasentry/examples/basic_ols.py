#!/usr/bin/env python

import os, sys 
import pandas as pd
import statsmodels.formula.api as smf
import pydatasentry 
from pydatasentry.lineage import track

if __name__ == "__main__": 


    pydatasentry.initialize()
    
    with track("load", 
               outputdatasets=['random'], 
               source="random" ):
        df = pd.DataFrame({"A": [10,20,30,40,50], 
                           "B": [20, 30, 10, 40, 50], 
                           "C": [32, 234, 23, 23, 42523]})
    
    with track("transform", "Merging two datasets", 
               inputdatasets=["random", "dist"], 
               outputdatasets=["random"]):
        print("Transforming") 

    result = smf.ols(formula="A ~ B + C", 
                     data=df, 
                     sentryopts={
                         'dataset': "random"
                     }
                 ).fit()

    #print(result.summary())
