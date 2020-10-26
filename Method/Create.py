# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 19:24:50 2020

@author: ghngu
"""


from Method.MethodB import MethodB
import Elastix.Elastix as Elastix


class CreateMethod(Base):
    
    def __init__(self):
        pass
        
    def SetParamSettings(self, settings):
        self.__derived.SetParamSettings(settings)
    
    def SetDataset(self, settings):
        self.__derived.SetDataset(settings)
        
    def SetValues(self, settings):
        self.__derived.SetValues(settings)
        
    def SetEnvironment(self, env):
        self.__derived.SetEnvironment(env)
        
    def Run(self):
        self.__derived.Run()
        
    def IsFinished():
        return self.__derived.IsFinished()
    
    def GetResultWithIndex(self, index):
        return self.__derived.GetResultWithIndex(index)
    
    def __Bind(self, derived):
        self.__derived = derived
        return self
    
    @staticmethod
    def CreateElastix():
        return __Bind(Elastix())
        
    