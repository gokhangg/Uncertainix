

import ExSettings.ParameterSettings as CreateParameterSettings
from Environment import Environment

class ExperimentSettings():
    
    def __init__(self, dataset):
        self.__dataset = dataset
        parameters = self.__dataset.GetMethodParameters()["MethodParameters"]
        self.__parameterSettings = CreateParameterSettings(parameters)
        self.__environment = Environment()
    
    def GetDataset(self, datasetIndex):
        return self.__dataset.GetDatasetWithIndex(datasetIndex)
    
    def GetParameterSettings(self, datasetIndex):
        return self.__parameterSettings(datasetIndex)
    
    def GetMethodParameters(self, datasetIndex):
        return self.__parameterSettings.GetParamValueSize()
    
    def SetParameterSettings(self, parameterSettings):
        self.__parameterSettings = parameterSettings
