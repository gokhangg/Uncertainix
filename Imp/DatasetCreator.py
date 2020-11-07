# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:19:07 2020

@author: ghngu
"""
from Dataset.RealImages.Dataset import  Dataset as RealImages
from Dataset.SynteticImages.Dataset  import Dataset as SynteticImages
from Dataset.RealImages.Environment import  Environment as RealEnvironment
from Dataset.SynteticImages.Environment  import Environment as SynteticEnvironment

from ExpSettings.DatasetBase import DatasetBase
from ExpSettings.EnvBase import EnvBase


def GetDataset(datasetType):
    if datasetType == "Real":
        return RealImages()
    if datasetType == "Synthetic":
        return SynteticImages()

def GetEnvironment(datasetType, rootDir):
    if datasetType == "Real":
        return RealEnvironment(rootDir)
    if datasetType == "Synthetic":
        return SynteticEnvironment(rootDir)
    
class Dataset_(DatasetBase):
    
    def __init__(self, dataset_):
        self.__dataset = dataset_
    
    def GetDatasetSize(self):
        return self.__dataset.GetDatasetSize()
    
    def GetDatasetWithIndex(self, ind:int):
        return self.__dataset.GetDatasetWithIndex(ind)
    
    def GetMethodParameters(self, ind:int):
        return self.__dataset.GetMethodParameters(ind)

class Environment_(EnvBase):
    
    def __init__(self, environment_):
        self.__dict = environment_.GetEnvironmentDict()
    
    def GetEnvironmentDict(self, el = {}):
        return self.__dict
        

class DatasetCreator(object):
    
    def __init__(self):
        pass
    
    @staticmethod
    def CreateDataset(datasetType):
        return Dataset_(GetDataset(datasetType))

    @staticmethod
    def CreateEnvironment(datasetType, rootDir):
        return Environment_(GetEnvironment(datasetType, rootDir))
    
 