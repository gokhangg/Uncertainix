# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 19:24:50 2020

@author: ghngu
"""


from Method.MethodB import MethodB as Base
from Elastix.ElastixHandler import Elastix


def CreateElastix() -> Base:
    return Elastix()
        
    