

import DatasetAndParameters.CreateDataset as CreateDataset
import DatasetAndParameters.ParameterSettings as CreateParameterSettings
from Environment import Environment

class ExperimentSettings():
    
    def __init__(self, datasetType):
        self.__dataset = CreateDataset(datasetType)
        parameters = self.__dataset.GetMethodParameters()["MethodParameters"]
        self.__parameterSettings = CreateParameterSettings(parameters)
        self.__environment = Environment()
    
    def GetDataset(self, datasetIndex):
        return self.__dataset.GetDatasetWithIndex(datasetIndex)
    
    def GetParameterSettings(self, datasetIndex):
        return self.__parameterSettings(datasetIndex)
    
    def GetNonrigCount(self, datasetIndex):
        return self.__parameterSettings.GetParamValueSize()
    
    def GetRigidElastixSettings(self, datasetIndex):
        return self.__dataset.GetRigidElastixDict()
    
    def GetRigidTransformixSettings(self, datasetIndex):
        return self.__dataset.GetNonrigidElastixDict()
    
    def GetNonrigidElastixSettings(self, datasetIndex):
        return self.__dataset.GetRigidTransformixDict()
    
    def GetNonrigidTransformixSettings(self, datasetIndex):
        return self.__dataset.GetNonrigidTransformixDict()
    
    def GetEnvironment(self):
        return self.__environment
    
    def SetParameterSettings(self, parameterSettings):
        self.__parameterSettings = parameterSettings
