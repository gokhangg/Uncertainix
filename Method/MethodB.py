# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 19:24:17 2020

@author: ghngu
"""

import abc


class MethodB(abc.ABC):
    
    @abc.abstractmethod
    def SetExperimentSettings(self):
        pass
    
    @abc.abstractmethod
    def Run(self):
        pass

    @abc.abstractmethod
    def IsFinished(self):
        pass    
    
    @abc.abstractmethod
    def GetResultWithIndex(self):
        pass
