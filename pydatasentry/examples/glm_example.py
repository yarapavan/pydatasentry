#!/usr/bin/env python

import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import pandas
import pydatasentry 

if __name__ == "__main__": 

    pydatasentry.initialize() 
    
    # http://statsmodels.sourceforge.net/devel/examples/notebooks/generated/glm_formula.html
    
    star98 = sm.datasets.star98.load_pandas().data
    formula = 'SUCCESS ~ LOWINC + PERASIAN + PERBLACK + PERHISP + PCTCHRT + \
    PCTYRRND + PERMINTE*AVYRSEXP*AVSALK + PERSPENK*PTRATIO*PCTAF'
    dta = star98[['NABOVE', 'NBELOW', 'LOWINC', 'PERASIAN', 'PERBLACK', 'PERHISP',
                  'PCTCHRT', 'PCTYRRND', 'PERMINTE', 'AVYRSEXP', 'AVSALK',
                  'PERSPENK', 'PTRATIO', 'PCTAF']]
    endog = dta['NABOVE'] / (dta['NABOVE'] + dta.pop('NBELOW'))
    del dta['NABOVE']
    dta['SUCCESS'] = endog
    
    mod1 = smf.glm(formula=formula, data=dta, family=sm.families.Binomial()).fit()
    mod1.summary()
