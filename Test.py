# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:16:55 2020

@author: ghngu
"""

from Imp.Imp import Implementation
from ItkHandler.ItkHandler import  ItkHandler
import os
selfDir = os.path.dirname(__file__)

imp = Implementation("SyntheticImages", selfDir)
imp.SelectMethod("TestMethod")
imp.SelectMode("MonteCarlo")
imp.Run(0)

imp.GetResult()





