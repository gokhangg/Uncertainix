# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 17:02:31 2020

@author: ghngu
"""
import abc

class EnvBase(abc.ABC):
    
    def __init__(self, rootDirectory: str):
        pass
    
    @abc.abstractmethod
    def GetEnvironmentDict(self):
        pass