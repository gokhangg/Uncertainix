# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:19:07 2020

@author: ghngu
"""
from Dataset.RealImages.ExperimentSettigs import  ExperimentSettigs as RealImagesExperimentSettigs
from Dataset.SynteticImages.ExperimentSettigs  import ExperimentSettigs as SynteticImagesExperimentSettigs



def GetExperimentSettings(datasetType, rootDir, index):
    if datasetType == "Real":
        return RealImagesExperimentSettigs(rootDir, index)
    if datasetType == "Synthetic":
        return SynteticImagesExperimentSettigs(rootDir, index)
        


class ExperimentSettings_():
    
    def __init__(self, experimentSettings):
        self.__experimentSettings = experimentSettings
        
    def GetDataset(self):
        return self.__experimentSettings.GetDataset()
    
  
    def GetMethodSettings(self, datasetIndex) -> dict:
        return self.__experimentSettings.GetMethodSettings()
    
    
    def GetModeSettings(self, datasetIndex) -> dict:
        return self.__experimentSettings.GetModeSettings()
    
    
    def SetParameters(self, parameters):
        self.__experimentSettings.SetParameters()
        
        
        
class ExperimentSettingsCreator(object):
    
    def __init__(self, datasetType):
        self.datasetType = datasetType
    
    def Create(self, rootDir: str, datasetIndex: int):
        exper = GetExperimentSettings(self.datasetType, rootDir, datasetIndex)
        
        return ExperimentSettings_(exper)

    
 