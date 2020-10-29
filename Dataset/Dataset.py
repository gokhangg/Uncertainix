# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:16:33 2020

@author: ghngu
"""

import abc

class DataSetBase(abc.ABC):
    
    @abc.abstractmethod
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def GetParams(self):
        pass
    
    @abc.abstractmethod
    def GetDataSetNum(self):
        pass
    
    @abc.abstractmethod
    def GetDatasetWithInd(self, ind):
        pass