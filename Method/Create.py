# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 19:24:50 2020

@author: ghngu
"""

from Method.MethodB import MethodB as Base

import importlib as imLib

def CreateMethod(method) -> Base:
    module_ = imLib.import_module("Method.{0:s}.Method".format(method))
    return module_.Method()
        
    