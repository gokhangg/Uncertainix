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


class ParameterSettings(object):
    __size = 1

    def __init__(self, parameters):
        self.__parameters = parameters
        self.__valueMappingFunctions = []
        for _ in range(len(self.__parameters)):
            self.__valueMappingFunctions.append(lambda a:a)
            
    
    def GetParamSize(self):
        return len(self.__parameters)
    
    def GetParamNames(self):
        names = [] 
        for param in self.__parameters:
            names.append(param.GetName())
            
    def GetParamValueSize(self):
        return len(self.__parameters[0].GetValues())
        
    def GetParamValues(self):
        values = [] 
        for param in self.__parameters:
            values.append(param.GetValues())
    
    def GetParamStatistics(self):
        statistics = []
        for param in self.__parameters:
            statistics.append(param.GetStatistics())
        
    def GetParamTypes(self):
        types = []
        for param in self.__parameters:
            types.append(param.GetType())
    
    def GetParamMethodParameters(self):
        methodParameters = []
        for param in self.__parameters:
            methodParameters.append(param.GetMethodParameters())
        return methodParameters 
        
        
    def SetParamValues(self, paramIndex, values):
        assert paramIndex < len(self.__parameters), "Parameter number mismatch."
        
        values = self.__MapParamVals(self, paramIndex, values)
        values = self.__ListToStr(values)
        self.__parameters[paramIndex].SetValues(values)
        
    def SaveParamValuesToFIle(self, file):
        pass
    
    def ReadParamValsFromFile(self, file):
        pass
    
    @classmethod
    def __MapParamVals(cls, paramIndex, values):
        for ind in range(len(values)):
            values[ind] = cls.__valueMappingFunctions[ind](values[ind])
        return values
    
    @staticmethod
    def __ListToStr(ls):
        retVal = []
        for par in ls:
            retVal.append(str(par))
        return retVal    