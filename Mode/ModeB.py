# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 20:13:19 2020

@author: ghngu
"""

import abc


class ModeB(abc.ABC):
    
    @abc.abstractmethod
    def SetModeSettings(self):
        pass
    
    @abc.abstractmethod
    def GetParameters():
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
    