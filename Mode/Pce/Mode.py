# *=========================================================================
# *
# *  Copyright Erasmus MC Rotterdam and contributors
# *  This software is licensed under the Apache 2 license, quoted below.

# *  Copyright 2019 Erasmus MC Rotterdam.
# *  Copyright 2019 Gokhan Gunay <g.gunay@erasmsumc.nl>

# *  Licensed under the Apache License, Version 2.0 (the "License"); you may not
# *  use this file except in compliance with the License. You may obtain a copy of
# *  the License at
# *  http://www.apache.org/licenses/LICENSE-2.0

# *  Unless required by applicable law or agreed to in writing, software
# *  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# *  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# *  License for the specific language governing permissions and limitations under
# *  the License.
# *=========================================================================

import numpy as np
import os, json

from Mode.ModeB import ModeB 

from pyPCE.pyPCE.SettingsFileIO import Settings as PceSettings
from pyPCE.pyPCE.ExampleSettingsFile import*
from pyPCE.pyPCE.pyPCE import pyPCE as PCE


class Mode(ModeB):
    
    def __init__(self):
        pass

    def SetModeSettings(self, settings):
        self.__parameters = settings["parameters"]
        self.__environment = settings["environment"]
        self.__extension = settings["extension"]
        self.__batchSize = self.__extension["batchSize"]
        settingsFile = self.__environment["pceModelSettingsFile"]
        
        if not os.path.isdir(self.__environment["experimentsRootDir"]):
            os.makedirs(self.__environment["experimentsRootDir"])
        outSettingsFile = self.__environment["experimentsRootDir"] + "/PceSettings.json"
        PceHandler.__UpdatePceParamFile(settingsFile, outSettingsFile, self.__parameters)

        pceSettings = PceSettings.LoadSettings(outSettingsFile)
        self.__pce = PCE(pceSettings)

        weights = self.__pce.GetModelInputSamplingScenarios()
        self.__sampleSize = len(weights[:, 0 ])
        for ind, it in enumerate(self.__parameters):
            it.SetRawValues(list(weights[:, ind] + it.GetStatistics()["mean"] ))
        
    
    def GetParameters(self):
        return self.__parameters
    
    def SetMethodOutput(self, MethodGetResultsReadyObj, MethodOutputObj):
        self.__methodGetResultsReadyObj = MethodGetResultsReadyObj
        self.__methodOutputObj = MethodOutputObj
    
    def Run(self):
        allVect = self.__GetAllData(self.__batchSize)
        self.__pce.SetModelOutput(allVect)
        self.__pce.CalculatePceCoefficients()
        print(5)

    def GetResult(self):
        return self.__pce.GetModelOutputStd([]).reshape(self.__dataShape)
    
    """
    @brief: Calculates standard deviation vector-image from several 
            deformation fields.
    @return: NA.
    """
    def __GetAllData(self, batchSize = 1):
        if batchSize == 0:
            batchSize = 1
        batchNum = int(self.__sampleSize / batchSize)
        batchRemnant = self.__sampleSize % batchSize

        for ind in range(batchNum):
            indices = [ind * batchSize + ii for ii in range(batchSize)]
            self.__methodGetResultsReadyObj(indices)
            for ind1 in indices:
                vect = np.array(self.__methodOutputObj(ind1), dtype = "float32")
                if ind1 == 0:
                    self.__dataShape = vect.shape
                    retVect = np.zeros([vect.size, self.__sampleSize], dtype = "float32")
                retVect[:, ind1] = vect.reshape(-1)

        indicesRemnant = [batchNum * batchSize + ii for ii in range(batchRemnant)]
        self.__methodGetResultsReadyObj(indicesRemnant)
        for ind1 in indicesRemnant:
            vect = self.__methodOutputObj(ind1)
            retVect[:, ind1] = vect.reshape(-1)
        return retVect
    


    @staticmethod
    def __GetPolynomialTypeFromDist(distribution):
        if distribution == "Gauss" or distribution == "gauss":
            return "hermite"
        if distribution == "Uniform" or distribution == "uniform":
            return "legendre"
        if distribution == "Exponential" or distribution == "exponential":
            return "laguerre"

    @staticmethod
    def __GetQuadratureTypeFromDist(distribution):
        if distribution == "Gauss" or distribution == "gauss":
            return "gauss-hermite"
        if distribution == "Uniform" or distribution == "uniform":
            return "gauss-legendre"
        if distribution == "Exponential" or distribution == "exponential":
            return "gauss-laguerre"

    @staticmethod
    def __SubUpdate(strings, settings, pceSettings):
        for strng in strings:
            if strng in settings:
                pceSettings[strng] = settings[strng]

    """
    @brief: Used to generate settings file for PCE executable as per PCE 
            settings.
    @return: NA.
    """
    @staticmethod
    def __UpdatePceParamFile(inFileName, outFileName, parameters, settings = dict()):
        with open(inFileName, "r") as fl:
            pceSettings  = json.load(fl)

        strings = ["pol_order", "grid_level", "grid_type", "trim", "remove_small_elements", "small_element_threshold"]
        PceHandler.__SubUpdate(strings, settings, pceSettings)
        
        quadType = []
        stdDevs = []
        polType = []
        for parameter in parameters:
            stat = parameter.GetStatistics()
            quadType += [PceHandler.__GetQuadratureTypeFromDist(stat["distribution"])]
            polType += [PceHandler.__GetPolynomialTypeFromDist(stat["distribution"])]
            stdDevs += [stat["std"]]
        pceSettings["quadrature_type"] = quadType
        pceSettings["pol_type"] = polType
        pceSettings["std_devs"] = stdDevs
        with open(outFileName, "w") as flOut:
            json.dump(pceSettings, flOut, indent = 2)
    



    """
    @brief: Runs PCE.
    @param: rigOnCluster Sets whether rigid registration will be executed on 
            computation cluster.
    @param: nonRigOnCluster Sets whether nonrigid registration will be executed 
            on computation cluster.
    @return: NA.
    """        
    def run(self, rigOnCluster = False, nonRigOnCluster = False):
        self.elastixOnCluster(rigOnCluster)
        self.runRig()
        self.generatePceParamFile()
        
        pceSettings = PceSettings.LoadSettings(self["PCE_ModelSetRunFile"])
        self.pce = pyPCE(pceSettings)
        self.loadWeightFromFile(self.pce.GetModelInputSamplingScenarios())
        
        self.__clusterWaitFunc()
        self.elastixOnCluster(nonRigOnCluster)
        self.runAllNonRigidReg()
        self.clusterWait()
        self.CalculatePceCoefficients()
        std = self.pce.GetModelOutputStd([])
        itkHandler = itk_handler()
        itkHandler.setImageVolumage(std.reshape(self.deformationFieldShape))
        itkHandler.setImageSpacing(self.deformationFieldSpacing)
        itkHandler.setImageOrigin(self.deformationFieldOrigin)
        itkHandler.saveImage(self["RegMainDir"] + "/std.mhd", True)
    
    """
    @brief: Generates standard image after all parameters are settled.
    @return: NA.
    """   
    def CalculatePceCoefficients(self):
        self["stdImageFile"] = self["RegMainDir"]+"/stdImage.mhd"
        for cnt in range(0, self.__sampleNum):
            self["defFieldDir"] = self["RegMainDir"] + "/NonRigid/Transformix" + str(cnt)
            self["nonRigRegDir"] = self["RegMainDir"] + "/NonRigid/Elastix" + str(cnt)
            self.getDeformationField()
            itkHandler = itk_handler()
            itkHandler.loadImage(self["RegMainDir"] + "/NonRigid/Transformix" + str(cnt) + "/deformationField.mhd")
            if cnt == 0:
                defField = itkHandler.getImageVolume()
                self.deformationFieldShape = defField.shape
                self.deformationFieldOrigin = itkHandler.getImageOrigin()
                self.deformationFieldSpacing = itkHandler.getImageSpacing()
                defField = defField.reshape(-1)
                self.deformationFieldSample = np.zeros([defField.shape[0], self.__sampleNum], dtype = "float")
            self.deformationFieldSample[:, cnt] = itkHandler.getImageVolume().reshape(-1)
        self.pce.SetModelOutput(self.deformationFieldSample)
        self.pce.CalculatePceCoefficients()

    """
        @brief: Implements all non rigid registrations.
        @return: NA.
    """
    def runAllNonRigidReg(self):
        for cnt in range(0, self.__sampleNum):
            self.runNonRigSingle(cnt)

    """
    @brief: Loads parameters to be analyzed.
    @param: file File name to load.
    @return: NA.
    """    
    def loadParamVals(self, file=""):
        if file == "":
            file = self["resultsRootDir"]+"/ParamVals.txt"
        if not os.path.isfile(file):
            assert("there is no file with the given name")   
        fl = open(file,"r")
        ln = fl.readlines()
        fl.close()
        self.__paramsToAnalyze=[]
        for it in ln:
            if it == "Param\n":
                self.__paramsToAnalyze += [Param()]
            elif it.count("Name"):
                self.__paramsToAnalyze[-1:][0].setName(it[len("Name") + 1:-1])
            elif it.count("Dist"):
                self.__paramsToAnalyze[-1:][0].setDist(it[len("Dist") + 1:-1])
            elif it.count("Mean"):
                self.__paramsToAnalyze[-1:][0].setMean(it[len("Mean") + 1:-1])
            elif it.count("Std"):
                self.__paramsToAnalyze[-1:][0].setStd(it[len("Std") + 1:-1])
            elif it.count("HighBnd"):
                self.__paramsToAnalyze[-1:][0].setHighBnd(it[len("HighBnd") + 1:-1])
            elif it.count("LowBnd"):
                self.__paramsToAnalyze[-1:][0].setLowBnd(it[len("LowBnd") + 1:-1])
            elif it.count("Size"):
                continue
            elif not it == "\n":
                self.__paramsToAnalyze[-1:][0].addRandVal(it)
                continue
    
    """
    @brief: Saves parameters to be analyzed.
    @param: file File name to save.
    @return: NA.
    """
    def saveParamVals(self, file = ""):
        if file == "":
            dr = self["resultsRootDir"]
            if not os.path.isdir(dr):
                os.makedirs(dr)
            file = dr + "/ParamVals.txt"
        fl=open(file, "w")
        for it in self.__paramsToAnalyze:
            fl.writelines("Param\n")
            fl.writelines("Name " + it.getName() + "\n")
            fl.writelines("Dist " + it.getDist() + "\n")
            fl.writelines("Mean " + str(it.getMean()) + "\n")
            fl.writelines("Std " + str(it.getStd()) + "\n")
            fl.writelines("HighBnd " + str(it.getHighBnd()) + "\n")
            fl.writelines("HighBnd " + str(it.getLowBnd()) + "\n")
            fl.writelines("Size " + str(it.getSize()) + "\n")
            vals = it.getRandVal()
            for i in vals:
                fl.writelines(str(i) + "\n")
            fl.writelines("\n")
        fl.close()
    
    
    
    """
    @brief: Used to generate weights file from PCE executable for registration sampling locations .
    @return: NA.
    """    
    def generateWeightFile(self):
        cmd = self["prePceCommands"]
        cmd += self["PCE_Exe"] + " -settingsFile " + self["PCE_ModelSetRunFile"] + " -writePceWeights " + self["Pce_WeightFile"]
        cmd += self["postPceCommands"]
        os.system(cmd)
    
    """
    @brief: Runs rigid registration.
    @return: NA.
    """ 
    def runRig(self):
        self["rigRegDir"] = self["RegMainDir"] + "/Rigid"
        if not os.path.exists(self["rigRegDir"]):
            os.makedirs(self["rigRegDir"])
        self.rigidElasRun()
    
    """
    @brief: Runs nonrigid registration.
    @return: NA.
    """ 
    def runNonRigSingle(self, ind):
        self["nonRigRegDir"] = self["RegMainDir"] + "/NonRigid/Elastix" + str(ind)
        paramDict = {}
        elasParamDict = {}
        for it in self.__paramsToAnalyze:
            paramDict.update({it.getName():it.getVals()[ind]})
            registrationParams = it["registrationParams"]
            for it2 in registrationParams:
                elasParamDict.update({it2:registrationParams[it2]})
        self.nonRigidElasRun(paramDict, elasParamDict)
    
    """
    @brief: Loads parameter values from a file with name embedded in 
            environment settings.
    @return: NA.
    """            
    def loadWeightFromFile(self, scenarios):
        self.setSampleNumber(scenarios.shape[0])
        if not scenarios.shape[1] == len(self.__paramsToAnalyze):
            assert("Parameter number mismatch.")
        for ind, it in enumerate(self.__paramsToAnalyze):
            it.resetVal()
            for ind2 in range(0, scenarios.shape[0]):
                it.addVal(float(scenarios[ind2, ind]) + it.getMean())
            it.mapVal()
            
    """
    @brief: Returns values of a parameter to be analyzed.
    @param: ind Parameter index in the parameter list.
    @return: Values of the parameters to be analyzed.
    """      
    def getParamVals(self,ind):
        return self.__paramsToAnalyze[ind].getVals()
    
    """
    @brief: Maps values of the parameters to be analyzed.
    @return: NA.
    """   
    def transParamVals(self):
        self.__weightsLs = self.__paramValTransFunc(self.__weightsLs)
      
    """
    @brief: Returns polynomial type of distributions.
    @param: dist Distribution.
    @return: Polynomial type.
    """
    def __getPolType(self,dist):
        if dist == "gauss":
            return "hermite"
        elif dist == "exponential":
            return "laguerre"
        elif self.__dist == "uniform":
            return "legendre"
        else:
            return ""
        
    """
    @brief: Used to add a new parameter to analyze.
    @param: param Parameter to be added.
    @return: NA.
    """
    def addParam(self, param):
        self.__paramsToAnalyze += [param]
    
    """
    @brief: Returns parameters to be analyzed.
    @return: Parameters to be analyzed.
    """
    def getParams(self):
        return self.__paramsToAnalyze

    """
    @brief: Sets all parameters in the analysis.
    @param: params Parameters to be set.
    @return: All parameters.
    """
    def setParams(self, params):
        self.__paramsToAnalyze = params
    
    """
    @brief: Sets polynomial order.
    @param: order Polynomial order.
    @return: NA.
    """
    def setPolOrder(self, order):
        self.__polOrd = order
    
    """
    @brief: Sets grid level.
    @param: level Grid level.
    @return: NA.
    """
    def setGridLevel(self, level):
        self.__gridLevel = level
    
    """
    @brief: Sets quadrature type.
    @param: quadType Quadrature type.
    @return: NA.
    """
    def setQuadratureType(self, quadType):
        self.__quadratureType = quadType
    
    """
    @brief: Sets grid type.
    @param: typ Grid type.
    @return: NA.
    """
    def setGridType(self, typ):
        self.__gridType = typ
    
    """
    @brief: Sets trim value.
    @param: trm Trim value.
    @return: NA.
    """
    def setTrim(self, trm):
        self.__trim = trm
    
    """
    @brief: Sets remove small elements token in the PCE settings.
    @param: rem Token for removal.
    @return: NA.
    """
    def setRemoveSmallElements(self, rem):
        self.__removeSmallElements = rem
    
    """
    @brief: Sets threshold for small elements token in the PCE settings.
    @param: thresh Threshold value.
    @return: NA.
    """
    def setSmallElementThresh(self, thresh):
        self.__smallElementThresh = thresh
    
    """
    @brief: Returns polynomial order.
    @return: Polynomial order.
    """
    def getPolOrder(self):
        return self.__polOrd
    
    """
    @brief: Returns grid level.
    @return: Grid level.
    """
    def getGridLevel(self):
        return self.__gridLevel
    
    """
    @brief: Returns quadrature type.
    @return: Quadrature type.
    """
    def getQuadratureType(self):
        quadType = []
        polType = self.getPolType()
        for it in polType:
            quadType += [self.__quadratureType + "-" + it]
        return quadType
    
    """
    @brief: Returns polynomial types of the parameter to be analyzed.
    @return: Polynomial types of the parameter to be analyzed.
    """    
    def getPolType(self):
        polType = []
        for it in self.__paramsToAnalyze:
            polType += [self.__getPolType(it.getDist())]
        return polType
    
    """
    @brief: Returns grid type.
    @return: Grid type.
    """
    def getGridType(self):
        return self.__gridType
    
    """
    @brief: Returns trim token.
    @return: Trim token.
    """
    def getTrim(self):
        return self.__trim
    
    """
    @brief: Returns remove small elements token in the PCE settings.
    @return: Remove small elements token in the PCE settings.
    """
    def getRemoveSmallElements(self):
        return self.__removeSmallElements
    
    """
    @brief: Returns threshold for small elements token in the PCE settings.
    @return: Threshold for small elements token in the PCE settings.
    """
    def getSmallElementThresh(self):
        return self.__smallElementThresh
    
    """
    @brief: Returns standard deviations of the parameters ot be analyzed.
    @return: Standard deviations of the parameters ot be analyzed.
    """
    def getStdDevs(self):
        stdDevs = []
        for it in self.__paramsToAnalyze:
            stdDevs += [str(it.getStd())]
        return stdDevs
    
    """
    @brief: Sets cluster waiting function.
    @param: waitFunc Waiting function.
    @return: NA.
    """   
    def setClusterWaitFunc(self, waitFunc):
        self.__clusterWaitFunc = waitFunc

    """
        @brief: Sets sample number.
        @param: sample number.
        @return: NA.
    """
    def setSampleNumber(self, num):
        self.__sampleNum = num

    """
        @brief: Gets sample number.
        @return: sample number.
    """
    def getSampleNumber(self):
        return self.__sampleNum
        
    """
    @brief: Waits cluster till finishing its job. This function is instantiated 
            with a lambda function returning True.
    @return: NA.
    """      
    def clusterWait(self):
        self.__clusterWaitFunc()
    
    """
    @brief: Assigns value for verbose execution.
    """
    def setVerbose(self, verb = False):
        self.__verbose = verb
    
    """
    @brief: Sets a function mapping values of the parameter.
            this funtion is instantiated by a lambda function returning back 
            its input.
    @param: func A function to map the parameter values.
    @return: NA.
    """
    def setParamValTransFunc(self, func):
        self.__paramValTransFunc = func
    
    """
    @brief: Sets an internal token for loading parameters from previous run.
    @param: fromPrevious Binary value to set the internal token.
    @return: NA.
    """
    def loadParamsFromPreviousRun(self, fromPrevious = False):
        self.__loadFrompreviousRun = fromPrevious
