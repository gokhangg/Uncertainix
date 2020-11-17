
from ExpSettings.ExperimentSettingsBase import ExperimentSettingsBase as Base

from ExpSettings.Dataset.RealImages.Dataset import Dataset as RealImages
from ExpSettings.Dataset.SyntheticImages.Dataset   import Dataset  as SyntheticImages
from ExpSettings.Dataset.RealImages.Environment import  Environment as RealImagesEnvironment
from ExpSettings.Dataset.SyntheticImages.Environment  import Environment  as SyntheticImagesEnvironment

def GetDataset2(datasetType):
    if datasetType == "Real":
        return RealImages()
    if datasetType == "Synthetic":
        return SyntheticImages()

def GetEnvironment(datasetType, rootDir):
    if datasetType == "Real":
        return RealImagesEnvironment(rootDir)
    if datasetType == "Synthetic":
        return SyntheticImagesEnvironment(rootDir)
        

class ExperimentSettings(Base):
    
    def __init__(self, rootDir: str, datasetType: str, datasetIndex: int):
        self.__dataset = GetDataset2(datasetType)
        self.__environment = GetEnvironment(datasetType, rootDir)
        self.__parameters = self.__dataset.GetParameters(datasetIndex)
        self.__datasetIndex = datasetIndex
    
    
    def GetMethodSettings(self):
        retVal =  {"parameters": self.__parameters}
        
        retVal.update( {"dataset": self.__dataset.GetDatasetWithIndex(self.__datasetIndex)} )
        retVal.update( {"extension": self.__dataset.GetMethodExtensionParams(self.__datasetIndex)} )
        retVal["extension"].update({"environment": self.__environment})
        
        return retVal
    
    
    def GetModeSettings(self):
        retVal =  {"parameters": self.__parameters}
        
        retVal.update( {"dataset": self.__dataset.GetDatasetWithIndex(self.__datasetIndex)} )
        retVal.update( {"extension": self.__dataset.GetModeExtensionParams(self.__datasetIndex)} )
        
        return retVal
    
    
    def SetParameters(self, parameters):
        self.__parameters = parameters