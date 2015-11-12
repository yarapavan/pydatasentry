#!/usr/bin/env python

from unittest import TestCase

import pydatasentry 

class TestBasic(TestCase):
    def test_basic(self):
        import pandas as pd 
        import statsmodels.formula.api as smf
        df = pd.DataFrame({"A": [10,20,30,40,50], 
                           "B": [20, 30, 10, 40, 50], 
                           "C": [32, 234, 23, 23, 42523]})
        result = smf.ols(formula="A ~ B + C", data=df).fit()
        self.assertTrue(result is not None)
