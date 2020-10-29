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
from Mode.ModeB import ModeB 


class MonteCarlo(ModeB):

    def SetStatSettings(self, settings):
        self.__sigma = settings["Sigma"]
        self.__mu = settings["Mean"]
        self.__distribution = settings["Distribution"]
        self.__sampleValues = self.__GetSampleVals()
    
    def SetSampleSize(self, sz):
        self.__sampleSize = sz
    
    def GetSampleVals(self):
        return self.__sampleValues
    
    def SetMethodOutput(self, MethodOutputObj):
        self.__methodOutputObj = MethodOutputObj
    
    def GetResult(self, ResType = {}):
        return self.__result
    
    def Run(self):
        self.__result = self.__GetStdVect()
    
    @staticmethod
    def __GetSampleSettings():
        settings = {}
        settings["SampleSize"] = 100
        settings["Sigma"] = [1., 2., 3.]
        settings["Mean"] = [0., 1., 2.]
        settings["Distribution"] = ["Gauss", "Gauss", "Gauss"]
        return settings


    """
    @brief: Calculates standard deviation vector-image from several 
            deformation fields.
    @return: NA.
    """
    def __GetStdVect(self):
        self.__pow2 = 0
        self.__sum = 0
        for ind in range(self.__sampleSize):
            vect = self.__methodOutputObj(ind)
            self.__pow2 += vect**2
            self.__sum += vect
        self.__sum /= self.__sampleNum
        self.__pow2 /= self.__sampleNum
        return np.sqrt(np.abs(self.__pow2 - self.__sum ** 2))

    def __GetSampleVals(self):
        retVal = self.__GetSampleVal(0)
        for ind in range(1, len(self.__mu)):
            np.concatenate((retVal, self.__GetSampleVal(ind)), 1)
        return retVal
    
    def __GetSampleVal(self, ind):
        if self.__distribution == "Gauss":
            return np.random.normal(self.__mu[ind], self.__sigma[ind], [self.__sampleSize, 1])
        
        
        