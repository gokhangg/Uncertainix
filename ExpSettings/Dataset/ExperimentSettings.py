
from ExpSettings.ExperimentSettingsBase import ExperimentSettingsBase as Base

from ExpSettings.Dataset.RealImages.Dataset import Dataset as RealImages
from ExpSettings.Dataset.SyntheticImages.Dataset   import Dataset  as SyntheticImages

def GetDataset(datasetType):
    if datasetType == "Real":
        return RealImages()
    if datasetType == "Synthetic":
        return SyntheticImages()        

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