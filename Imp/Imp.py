

from Mode import Create as CreateMode
from Method import Create as CreateMethod
from ExpSettings.Dataset.ExperimentSettings import ExperimentSettings
from ItkHandler.ItkHandler import  ItkHandler

import importlib as imLib
import time

class Implementation():
    
    def __init__(self, datasetType: str, rootDir: str):
        self.__itkHandler = ItkHandler()
        self.__datasetType = datasetType
        self.__rootDir = rootDir
        self.__sampleSize = 100
    
    def SelectMode(self, mode):
        self.__mode = CreateMode.CreateMode(mode)
        self.__modeName = mode
    
    def SelectMethod(self, method):
        self.__method = CreateMethod.CreateMethod(method)
        self.__methodName = method
            
    def SetSampleSize(self, size):
        self.__sampleSize = size
            
    def Run(self, datasetIndex = 0):
        self.__experSettings = ExperimentSettings( self.__rootDir, self.__datasetType, datasetIndex)

        """
        Since the environment class is propagated through method and mode classes, a change in it in a place
        also propagates other locations.
        """
        self.__experSettings.GetMethodSettings()["environment"]["experimentsRootDir"] += "/" + self.__modeName
        
        modeSettings = self.__experSettings.GetModeSettings()
        self.__mode.SetModeSettings(modeSettings)
        parameters = self.__mode.GetParameters()
        self.__experSettings.SetParameters(parameters)
        
        methodSettings = self.__experSettings.GetMethodSettings()
        self.__method.SetMethodSettings(methodSettings)
        self.__method.Run(datasetIndex)
        while not self.__method.IsFinished():
            time.sleep(25)
        
        self.__mode.SetMethodOutput(self.__method.GetResultsReady, self.__GetResultforMode)
        
        self.__mode.Run()
        
    def GetResult(self):
        im_ = [self.__mode.GetResult(), self.__resultImageOrigin, self.__resultImageSpacing]
        methodSettings = self.__experSettings.GetMethodSettings()
        if methodSettings["environment"]["finalResultFile"] is not None:
            ItkHandler.SaveItkImage(methodSettings["environment"]["finalResultFile"], im_, isVector=True)

    def __GetResultforMode(self, index):
        _, itkIm = self.__method.GetResultWithIndex(index)
        if index == 0:
            self.__resultImageOrigin = itkIm.GetImageOrigin()
            self.__resultImageSpacing = itkIm.GetImageSpacing()
        itkIm
        return itkIm.GetImageVolume()
        



    
    
    

