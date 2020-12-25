

from Mode import Create as CreateMode
from Method import Create as CreateMethod
from ExpSettings.Dataset.ExperimentSettings import ExperimentSettings
from ItkHandler.ItkHandler import  ItkHandler

import importlib as imLib
import time, os

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
    
    def SetDatasetIndex(self, index):
        self.__datasetIndex = index
            
    def Run(self):
        self.__experSettings = ExperimentSettings( self.__rootDir, self.__datasetType, datasetIndex)

        """
        Since the environment class is propagated through method and mode classes, a change in it in a place
        also propagates other locations.
        """
        experimentRootDir = self.__experSettings.GetMethodSettings()["environment"]["experimentsRootDir"]
        experimentRootDir += "/" + self.__modeName
        self.__experSettings.GetMethodSettings()["environment"]["experimentsRootDir"] = experimentRootDir

        if not os.path.isdir(experimentRootDir):
            os.makedirs(experimentRootDir)

        
        modeSettings = self.__experSettings.GetModeSettings()
        self.__mode.SetModeSettings(modeSettings)
        parameters = self.__mode.GetParameters()
        self.__experSettings.SetParameters(parameters)
        
        methodSettings = self.__experSettings.GetMethodSettings()
        self.__method.SetMethodSettings(methodSettings)
        self.__method.Run(self.__datasetIndex)
        while not self.__method.IsFinished():
            print("Sleeping for {0:d} seconds.".format(25))
            time.sleep(25)
        
        self.__mode.SetMethodOutput(self.__method.GetResultsReady, self.__GetResultforMode)
        
        self.__mode.Run()
        
    def GetResult(self):
        im_ = [self.__mode.GetResult(), self.__resultImageOrigin, self.__resultImageSpacing]
        modeSettings = self.__experSettings.GetModeSettings()
        resFile = modeSettings["environment"]["finalResultFile"]
        isVector = modeSettings["extension"]["isVector"]
        if resFile is not None:
            ItkHandler.SaveItkImage(resFile, im_, isVector)
            return resFile
        return ""

    def __GetResultforMode(self, index):
        itkIm = self.__method.GetResultWithIndex(index)
        if index == 0:
            self.__resultImageOrigin = itkIm.GetImageOrigin()
            self.__resultImageSpacing = itkIm.GetImageSpacing()
        itkIm
        return itkIm.GetImageVolume()
        



    
    
    

