# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:16:55 2020

@author: ghngu
"""

from Imp.Imp import Implementation


imp = Implementation("Real", "ExperimentResults")
imp.SelectMethod("Elastix")
imp.SelectMode("MonteCarlo")
imp.Run(0)