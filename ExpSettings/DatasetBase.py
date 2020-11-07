# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:16:33 2020

@author: ghngu
"""

import abc

class DatasetBase(abc.ABC):
    
    @abc.abstractmethod
    def GetDatasetSize(self):
        pass
    
    @abc.abstractmethod
    def GetDatasetWithIndex(self, ind:int):
        pass
    
    @abc.abstractmethod
    def GetMethodParameters(self, ind:int):
        pass