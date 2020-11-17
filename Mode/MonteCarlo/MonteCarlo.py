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

    
    def SetModeSettings(self, settings):
        parameters = settings["parameters"]
        self.__sampleSize = settings["extension"]["sampleSize"]
        
        for it in parameters:
            it.SetRawValues(self.__GetSampleVal(it, self.__sampleSize))
        self.__parameters = parameters
    
    def SetSampleSize(self, sz):
        self.__sampleSize = sz
    
    def GetParameters(self):
        return self.__parameters
    
    def SetMethodOutput(self, MethodOutputObj):
        self.__methodOutputObj = MethodOutputObj
    
    def GetResult(self, ResType = {}):
        return self.__result
    
    def Run(self):
        self.__result = self.__GetStdVect()


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
    
    @staticmethod
    def __GetSampleVal(parameter, sampleSize):
        stat = parameter.GetStatistics()
        if stat["distribution"] == "Gauss" or stat["Distribution"] == "gauss":
            return np.random.normal(float(stat["mean"]), float(stat["std"]), [sampleSize, 1])
        
        
        
