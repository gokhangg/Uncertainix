# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:16:55 2020

@author: ghngu
"""

from Imp.Imp import Implementation
import os
selfDir = os.path.dirname(__file__)

imp = Implementation("Real", selfDir + "/ExperimentResults")
imp.SelectMethod("Elastix")
imp.SelectMode("MonteCarlo")
imp.Run(0)