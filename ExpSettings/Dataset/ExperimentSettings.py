
from ExpSettings.ExperimentSettingsBase import ExperimentSettingsBase as Base

import importlib as imLib

"""
!!! Place where string based module import is done.

"""
def GetDataset(datasetType):
    module_ =  imLib.import_module("ExpSettings.Dataset.{0:s}.Dataset".format(datasetType))
    return module_.Dataset()

class ExperimentSettings(Base):
    
    def __init__(self, rootDir: str, datasetType: str, datasetIndex: int):
        self.__dataset = GetDataset(datasetType)
        self.__environment = self.__dataset.GetEnvironment(rootDir)
        self.__parameters = self.__dataset.GetParameters(datasetIndex)
        self.__datasetIndex = datasetIndex
    
    def GetMethodSettings(self):
        retVal =  {"parameters": self.__parameters}
        retVal.update( {"dataset": self.__dataset.GetDatasetWithIndex(self.__datasetIndex)} )
        retVal.update({"environment": self.__environment})
        retVal.update( {"extension": self.__dataset.GetMethodExtensionParams(self.__datasetIndex)} )
        
        return retVal
    
    
    def GetModeSettings(self):
        retVal =  {"parameters": self.__parameters}
        retVal.update( {"dataset": self.__dataset.GetDatasetWithIndex(self.__datasetIndex)} )
        retVal.update({"environment": self.__environment})
        retVal.update( {"extension": self.__dataset.GetModeExtensionParams(self.__datasetIndex)} )
        
        return retVal
    
    
    def SetParameters(self, parameters):
        self.__parameters = parameters