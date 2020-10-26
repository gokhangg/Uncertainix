# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 21:08:55 2020

@author: ghngu
"""

from MonteCarlo.MonteCarlo import MonteCarlo as MC
from PceHandler.pcehandler import PCE as PCE
from Mode.ModeB import ModeB


class CreateMode(ModeB):
    
    def __init__(self):
        pass
        
    def SetStatSettings(self, settings):
        self.__derived.SetSettings(settings)
    
    def GetSampleSize(self):
        return self.__derived.GetSampleSize()
    
    def SetSampleSize(self, sz):
        return self.__derived.SetSampleSize(sz)
    
    def GetSampleVals(self):
        return self.__derived.GetSampleVals()
    
    def SetSampleVals(self, sampleVals):
        return self.__derived.SetSampleVals(sampleVals)
    
    def SetMethodOutput(self, MethodOutputObj):
        return self.__derived.SetMethodOutput(MethodOutputObj)
    
    def Run(self):
        return self.__derived.Run()
    
    def GetResult(self, ResType = {}):
        return self.__derived.GetResult(ResType)
    
    @classmethod
    def Bind(cls, derived):
        cls.__derived = derived
        return cls
    
    @staticmethod
    def CreatePce():
        return CreateMode.Bind(Pce())

    @staticmethod
    def CreateMc():
        return CreateMode.Bind(MC())