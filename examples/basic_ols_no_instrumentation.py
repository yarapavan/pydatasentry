#!/usr/bin/env python

import os, sys 
import pandas as pd
import statsmodels.formula.api as smf

if __name__ == "__main__": 

    print("Came here")
    df = pd.DataFrame({"A": [10,20,30,40,50], 
                       "B": [20, 30, 10, 40, 50], 
                       "C": [32, 234, 23, 23, 42523]})
    result = smf.ols(formula="A ~ B + C", 
                     data=df
                 ).fit()

    print(result.summary())
