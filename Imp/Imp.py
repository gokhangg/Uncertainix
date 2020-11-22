

from Mode import Create as CreateMode
from Method import Create as CreateMethod
from ExpSettings.Dataset.ExperimentSettings import ExperimentSettings
from ItkHandler.ItkHandler import  ItkHandler

import time

class Implementation():
    
    def __init__(self, datasetType: str, rootDir: str):
        self.__itkHandler = ItkHandler()
        self.__datasetType = datasetType
        self.__rootDir = rootDir
        self.__sampleSize = 100
    
    def SelectMode(self, mode):
        if mode == "MonteCarlo":
            self.__mode = CreateMode.CreateMc()
        elif mode == "PCE":
            self.__mode = CreateMode.CreatePce()
        self.__modeName = mode
    
    def SelectMethod(self, method):
        if method == "Elastix":
            self.__method = CreateMethod.CreateElastix()

            
    def SetSampleSize(self, size):
        self.__sampleSize = size
            
    def Run(self, datasetIndex = 0):
        self.__experSettings = ExperimentSettings( self.__rootDir, self.__datasetType,datasetIndex)
        
        
        modeSettings = self.__experSettings.GetModeSettings()
        self.__mode.SetModeSettings(modeSettings)
        parameters = self.__mode.GetParameters()
        self.__experSettings.SetParameters(parameters)
        
        methodSettings = self.__experSettings.GetMethodSettings()
        if methodSettings["environment"]["experimentsRootDir"] is not None:
            methodSettings["environment"]["experimentsRootDir"] += "/" + self.__modeName
        self.__method.SetMethodSettings(methodSettings)
        self.__method.Run(datasetIndex)
        while not self.__method.IsFinished():
            time.sleep(25)
        
        self.__mode.SetMethodOutput(self.__method.GetResultsReady, self.__GetResultforMode)
        
        self.__mode.Run()
        
    def GetResult(self):
        return self.__mode.GetResult()

    def __GetResultforMode(self, index):
        _, itkIm = self.__method.GetResultWithIndex(index)
        return itkIm.GetImageVolume()
        



    
    
    

