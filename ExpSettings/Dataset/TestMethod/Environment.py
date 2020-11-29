# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 17:02:31 2020

@author: ghngu
"""


from ExpSettings.EnvBase import EnvBase

import sys, time,os 

_selfPath = os.path.dirname(__file__)


class Environment(EnvBase):
    
    def __init__(self, rootDirectory):
        self.__rootDictionary = {}
        #Root Dir where the results to be saved
        self["rootDir"] = rootDirectory

        #Settings file for PCE execution model
        self["pceModelSetRunFile"] = _selfPath + "/PCE_Settings.json"

    def GetRootEnvironmentDict(self):
        return self.__rootDictionary
    
    def GetEnvironmentDictForDataset(self, datasetIndex, expSize, el = {}):
        envDict = self.__rootDictionary
        return envDict
        
    def __getitem__(self, key):
        if key in self.__rootDictionary:
            return self.__rootDictionary[key]
        return None
    
    def __setitem__(self, key, val):
        self.__rootDictionary.update({key : val})
        