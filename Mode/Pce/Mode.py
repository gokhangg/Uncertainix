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
        Mode.__UpdatePceParamFile(settingsFile, outSettingsFile, self.__parameters)

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
        Mode.__SubUpdate(strings, settings, pceSettings)
        
        quadType = []
        stdDevs = []
        polType = []
        for parameter in parameters:
            stat = parameter.GetStatistics()
            quadType += [Mode.__GetQuadratureTypeFromDist(stat["distribution"])]
            polType += [Mode.__GetPolynomialTypeFromDist(stat["distribution"])]
            stdDevs += [stat["std"]]
        pceSettings["quadrature_type"] = quadType
        pceSettings["pol_type"] = polType
        pceSettings["std_devs"] = stdDevs
        with open(outFileName, "w") as flOut:
            json.dump(pceSettings, flOut, indent = 2)
    