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

#sys.path.insert(0,"./lib")

from ElastixHandler import* 

class ImageStatistics(Elastix):
    __verbose=False
    
    def __init__(self):
        super(ImageStatistics, self).__init__()
        self.__meanArr=[0.0]
        self.__stdArr=[1.0]
        self.__sampleNum=10
        self.__randVarTypeArr=["gauss"]
    
    def setClusterWaitFunc(self,waitFunc):
        self.__clusterWaitFunc=waitFunc
    
    def setVerbose(self,verb=False):
        self.__verbose=verb
        
    def setMean(self,arr=[0.0]):
        self.__meanArr=arr
    
    def setStd(self,arr=[1.0]):
        self.__stdArr=arr
        
    def setSampleNum(self,sn=10):
        self.__sampleNum=sn
    
    def setRandVarType(self,varType=["gauss"]):
        self.__randVarTypeArr=varType 
    
    def setParamName(self,paramNames=[""]):
        self.__paramNameArr=paramNames 
        
    def __getRandVal(self,std=1,mean=0,varType=["gauss"],sz=1):
        if varType=="gauss":
            return np.random.normal(mean,std,sz)
        elif varType=="exponential":
            return np.random.exponential(std,sz)
        elif varType=="uniform":
            low=mean
            high=std
            return np.random.uniform(low,high,sz)
        
    def generateParamVals(self):
        if not (len(self.__stdArr)==len(self.__meanArr) and len(self.__stdArr)==len(self.__randVarTypeArr)):
            if self.__verbose:
                print("Std and Mean and VarType lengths are not compatible, returning none")
                return []
        ls=[]
        print(self.__stdArr)
        print(self.__meanArr)
        print(self.__randVarTypeArr)
        for std,mean,varType in list(map(list,zip(*[self.__stdArr,self.__meanArr,self.__randVarTypeArr]))):
            ls+=[self.__getRandVal(std,mean,varType,sz=self.__sampleNum)]
        self.__weightsLs=ls
        return ls
    
    def saveParamVals(self, file=""):
        if not len(file)>0:
            file=self.elas.env["resultsRootDir"]+"/ParamVals.txt"
        fl=open(file,"w")
        for cnt in range(0,len(self.__weightsLs)):
            fl.writelines("Param "+str(cnt)+" Vals\n")
            fl.writelines(str(self.__weightsLs[cnt])+"\n")
        fl.close()
    
    def run(self,cnt):
        self.setSampleNum(cnt)
        self.generateParamVals()
        self.saveParamVals()
        self.elas.rigidTransRun()
        self.__clusterWaitFunc()
        self.elas.nonRigidTransRun(ParamDict={"Metric1Weight":"256"})
        
