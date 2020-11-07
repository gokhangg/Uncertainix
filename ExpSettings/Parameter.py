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


class Parameter(object):
    """
    @brief: Init.
    @param: name Name of the Elastix parameter.
    @param: dist Distribution of the parameter.
    @param: mean Mean of the parameter.
    @param: std Standard deviation of the parameter.
    @param: low If parameter distribution is union sets lower boundary.
    @param: high If parameter distribution is union sets higher boundary.
    @return: NA.
    """ 
    def __init__(self, name = "", dist = "", mean = 0, std = 1, low = 0, high = 1, valType = float):
        self.__name = name
        self.__std = std
        self.__mean = mean
        self.__dist = dist
        self.__lowBnd = low
        self.__highBnd = high
        self.__valType = valType
        self.__vals = []
        
    def GetName(self):
        return self.__name
    
    def GetValues(self):
        return self.__vals
    
    def GetStatistics(self):
        retDict = {}
        retDict.update({"Distribution":self.__dist})
        retDict.update({"Std":str(self.__std)})
        retDict.update({"Mean":str(self.__mean)})
        retDict.update({"LowBoundary":str(self.__lowBnd)})
        retDict.update({"HighBoundary":str(self.__highBnd)})
        return retDict
    
    def SetValues(self, values):
        self.__vals = values
        
    def GetValType(self):
        return self.__valType
    
    
