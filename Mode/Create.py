# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 21:08:55 2020

@author: ghngu
"""

import importlib as imLib

def CreateMode(mode):
    module_ = imLib.import_module("Mode.{0:s}.Mode".format(mode))
    return module_.Mode()