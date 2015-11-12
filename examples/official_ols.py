#!/usr/bin/env python 

#!/usr/bin/env python

import statsmodels.formula.api as smf
import statsmodels.api as sm 
import numpy as np
import pandas
import pydatasentry 

if __name__ == "__main__": 
    pydatasentry.initialize() 

    df = sm.datasets.get_rdataset("Guerry", "HistData").data
    df = df[['Lottery', 'Literacy', 'Wealth', 'Region']].dropna()
    df.head()
    mod = smf.ols(formula='Lottery ~ Literacy + Wealth + Region', 
                  data=df)
    res = mod.fit()
    print(res.summary())
    
