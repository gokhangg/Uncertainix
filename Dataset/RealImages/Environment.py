# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 17:02:31 2020

@author: ghngu
"""


class Environment():
    
    def __init__(self, rootDirectory):
        self.__dictionary = {}
        #Root Dir where the results to be saved
        self["RootDir"] = rootDirectory
        self["resultsRootDir"] = self["RootDir"] + "/temp/ExpResults/MC"
        #Rootdir where registration results to be saved
        self["registRootDir"] = self["resultsRootDir"]
        
        
        #Settings file for PCE execution model
        self["PCE_ModelSetRunFile"] = "/PCE_Settings.json"
        #Elastix executable 
        self["elastixExe"] = "/home/gogo/Tools/elastix-5.0.0/bin/bin/elastix"
        #Transformix executable
        self["transformixExe"] = "/home/gogo/Tools/elastix-5.0.0/bin/bin/transformix"
    
    def GetEnvironmentDict(self, el = {}):
        return self.__dictionary
        
    def __getitem__(self, key):
        if key in self.__dictionary:
            return self.__dictionary[key]
        return None
    
    def __setitem__(self, key, val):
        self.__dictionary.update({key : val})