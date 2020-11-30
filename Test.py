# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:16:55 2020

@author: ghngu
"""

from Imp.Imp import Implementation
from ItkHandler.ItkHandler import  ItkHandler
import os
selfDir = os.path.dirname(__file__)

"""Generating Results for Pce and MC for 10 datasets"""
for mode_ in ["MonteCarlo", "Pce"]:
    for ind in range(10):
        imp = Implementation("SyntheticImages", selfDir)
        imp.SelectMethod("Elastix")
        imp.SelectMode(mode_)
        imp.Run(ind)

        imp.GetResult()





