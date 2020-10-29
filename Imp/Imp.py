

from Mode import Create as CreateMode
from Method.Create.Create import CreateMethod
import Environment.EnvSetup.Environment as Environment
import ItkHandler.itk_handler.itk_handler as ItkHandler
import Dataset.RealImages.Dataset as RealDataset
import Dataset.SynteticImages.Dataset as SimDataset

import time



class Implementation():
    
    def __init__(self):
        self.__itkHandler = ItkHandler()
        self.__env = Environment()
        self.__sampleSize = 100
    
    def SelectMode(self, mode):
        if mode == "MonteCarlo":
            self.__mode = CreateMode.CreateMc()
        elif mode == "PCE":
            self.__mode = CreateMode.CreatePce()
    
    def SelectMethod(self, method):
        if method == "Elastix":
            self.__method = CreateMethod.CreateElastix()
        self.__method.SetEnvironment(self.__env)
            
    def SelectDataset(self, dataset):
        if dataset == "RealDataset":
            self.__dataset = RealDataset()
        elif dataset == "SimulatedDataset":
            self.__dataset = SimDataset()
            
    def SetSampleSize(self, size):
        self.__sampleSize = size
            
    def Run(self, datasetIndex = 0):
        paramSettings = self.__dataset.GetParams()
        
        self.__mode.SetStatSettings(paramSettings)
        self.__mode.SetSampleSize(self.__sampleSize)
        paramVals = self.__mode.GetSampleVals()
        
        dataset = self.__dataset.GetDatasetWithIndex(datasetIndex)
        self.__method.SetDataset(dataset)
        self.__method.SetParamSettings(paramSettings)
        self.__method.SetEnvironment(self.__env)
        self.__method.SetParamVals(paramVals)
        
        self.__method.Run()
        while not self.__method.IsFinished():
            time.sleep(25)
        
        resultFunct = self.__method.GetResultWithIndex
        self.__mode.SetMethodOutput(resultFunct)
        
        self.__mode.Run()
        
    def GetResult(self):
        return self.__mode.GetResult()