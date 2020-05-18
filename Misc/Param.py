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

class Param(object):
    __size = 1

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
    def __init__(self, name = "", dist = "", mean = 0, std = 1, low = 0, high = 1):
        self.__name = name
        self.__std = std
        self.__mean = mean
        self.__dist = dist
        self.__lowBnd = low
        self.__highBnd = high
        self.__vals = np.zeros(0)
        self.__params = {}
        self.__transFunct = lambda param:param
    
    """
    @brief: Loads the parameter from a files.
    @param: file File name to load the parameter.
    @return: Returns success token of the attempt.
    """  
    def loadFromFile(self, file=""):
        try:
            fl=open(file,"r")
        except:
            return False
        self.resetVal()
        ln=fl.readlines()
        fl.close()
        for it in ln:
            if it.count("Name"):
                self.setName(it[len("Name")+1:-1])
            elif it.count("Dist"):
                self.setDist(it[len("Dist")+1:-1])
            elif it.count("Mean"):
                self.setMean(it[len("Mean")+1:-1])
            elif it.count("Std"):
                self.setStd(it[len("Std")+1:-1])
            elif it.count("HighBnd"):
                self.setHighBnd(it[len("HighBnd")+1:-1])
            elif it.count("LowBnd"):
                self.setLowBnd(it[len("LowBnd")+1:-1])
            elif it.count("Size"):
                continue
            elif not it=="\n":
                self.addVal(it)
                continue
        return True
    
    """
    @brief: Saves the parameter to a files.
    @param: file File name to save the parameter.
    @return: Returns success token of the attempt.
    """    
    def saveToFile(self, file = ""):
        try:
            fl = open(file, "w")
        except:
            return False
        fl.writelines("Name "+self.getName() + "\n")
        fl.writelines("Dist "+self.getDist() + "\n")
        fl.writelines("Mean "+str(self.getMean()) + "\n")
        fl.writelines("Std "+str(self.getStd()) + "\n")
        fl.writelines("HighBnd "+str(self.getHighBnd()) + "\n")
        fl.writelines("LowBnd "+str(self.getLowBnd()) + "\n")
        fl.writelines("Size "+str(self.getSize()) + "\n")
        vals = self.getVals()
        for it in vals:
            fl.writelines(str(it) + "\n")
        fl.writelines("\n")
        fl.close()
        return True
    
    """
    @brief: Maps values of the parameter and writes back.
    @return: NA.
    """
    def mapVal(self):
        self.__vals=self.__transFunct(self.__vals)   
        
    """
    @brief: Sets a function mapping values of the parameter.
            this funtion is instantiated by a lambda function returning back 
            its input.
    @param: func A function to map the parameter values.
    @return: NA.
    """
    def setValMapFunct(self,func):
        self.__transFunct=func

    """
    @brief: Adds a new element to vector with random values.
    @return: NA.
    """
    def addVal(self,val):
        self.__vals=np.append(self.__vals,float(val))
     
    """
    @brief: Fills vector with random values as per parameter statistics.
    @return: NA.
    """
    def generateRandVal(self):
        if self.__dist=="gauss":
            self.__vals= np.random.normal(self.__mean,self.__std,self.__size)
        elif self.__dist=="exponential":
            self.__vals= np.random.exponential(self.__std,self.__size)
        elif self.__dist=="uniform":
            self.__vals= np.random.uniform(self.__lowBnd,self.__highBnd,self.__size)
        else:
            self.__vals= np.zeros(0)
    
    """
    @brief: Sets name of the parameter.
    @return: NA.
    """
    def setName(self,name):
        self.__name=name
    
    """
    @brief: Sets distribution of the parameter.
    @return: NA.
    """
    def setDist(self,dist):
        self.__dist=dist
    
    """
    @brief: Sets mean of the parameter.
    @return: NA.
    """
    def setMean(self,mean):
        self.__mean=float(mean)
    
    """
    @brief: Sets standard deviation of the parameter.
    @return: NA.
    """
    def setStd(self,std):
        self.__std=float(std)
    
    """
    @brief: If the variable is uniform, sets higher boundary of the parameter.
    @return: NA.
    """
    def setHighBnd(self,high):
        self.__highBnd=float(high)
    
    """
    @brief: If the variable is uniform, sets lower boundary of the parameter.
    @return: NA.
    """
    def setLowBnd(self,low):
        self.__lowBnd=float(low)
    
    """
    @brief: Sets vector length of the parameter.
    @return: NA.
    """
    def setSize(self,size):
        self.__size=int(size)
    
    """
    @brief: Gets name of the parameter.
    @return: Name of the parameter.
    """
    def getName(self):
        return self.__name
    
    """
    @brief: Gets distribution of the parameter.
    @return: Distribution of the parameter.
    """
    def getDist(self):
        return self.__dist
     
    """
    @brief: Gets mean of the parameter.
    @return: Mean of the parameter.
    """
    def getMean(self):
        return self.__mean
    
    """
    @brief: Gets standard deviation of the parameter.
    @return: Standard deviation of the parameter.
    """
    def getStd(self):
        return self.__std
     
    """
    @brief: If the variable is uniform, gets higher boundary of the parameter.
    @return: Higher boundary of the parameter.
    """
    def getHighBnd(self):
        return self.__highBnd
    
    """
    @brief: If the variable is uniform, gets lower boundary of the parameter.
    @return: Lower boundary of the parameter.
    """
    def getLowBnd(self):
        return self.__lowBnd
    
    """
    @brief: Gets vector length of the parameter.
    @return: Vector length of the parameter.
    """
    def getSize(self):
        return len(self.__vals) 
    
    """
    @brief: Gets vector with random values.
    @return: Vector with random values.
    """
    def getVals(self):
        return self.__vals
    
    """
    @brief: If vector with random values is desired to be filled from outside.
    @return: NA.
    """
    def setVals(self,vals):
        self.__vals=np.array(vals)
    
    """
    @brief: Zeros vector with random values.
    @return: NA.
    """
    def resetVal(self):
        self.__vals=np.zeros(0)

    def __getitem__(self,key):
        try:
            return self.__params[key]
        except:
            return ""
        
    def __setitem__(self,key,val):
        self.__params.update({key:val})