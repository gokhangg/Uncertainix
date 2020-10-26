# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 20:13:19 2020

@author: ghngu
"""

import abc


class ModeB(abc.ABC):
    
    @abc.abstractmethod
    def SetStatSettings(self):
        pass
    
    @abc.abstractmethod
    def GetSampleSize(self):
        pass
    
    @abc.abstractmethod
    def SetSampleSize(self):
        pass
    
    @abc.abstractmethod
    def GetSampleVals(self):
        pass
    
    @abc.abstractmethod
    def SetSampleVals(self):
        pass
    
    @abc.abstractmethod
    def SetMethodOutput(self):
        pass
    
    @abc.abstractmethod
    def GetResult(self):
        pass
    
    @abc.abstractmethod
    def Run(self):
        pass
    