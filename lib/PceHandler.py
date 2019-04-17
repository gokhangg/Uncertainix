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
import os,shutil

from ElastixHandler import* 
from Param import* 

class PceHandler(Elastix):
    __verbose=False
    
    def __init__(self):
        super(PceHandler, self).__init__()
        self.__sampleNum=10
        self.__paramsToAnalyze=[]
        self.__polOrd=1
        self.__gridLevel=1
        self.__quadratureType=[]
        self.__gridType="sparse"
        self.__trim="1"
        self.__removeSmallElements="1"
        self.__smallElementThresh="1e-13"
        self.__selfParams={}
        self.__clusterWaitFunc=lambda:True
        self.__paramValTransFunc=lambda params:params
        self.__loadFrompreviousRun=False
    
    """
    @brief: Runs PCE.
    @param: rigOnCluster Sets whether rigid registration will be executed on 
            computation cluster.
    @param: nonRigOnCluster Sets whether nonrigid registration will be executed 
            on computation cluster.
    @return: NA.
    """        
    def run(self,rigOnCluster=False,nonRigOnCluster=False):
        self.elastixOnCluster(rigOnCluster)
        self.runRig()
        self.generatePceParamFile()
        self.generateWeightFile()
        self.loadWeightFromFile()
        self.__clusterWaitFunc()
        self.elastixOnCluster(nonRigOnCluster)
        for cnt in range(0,self.__sampleNum):
            self.runNonRigSingle(cnt)
        self.clusterWait()
        self.getStd()
    
    """
    @brief: Generates standard image after all parameters are settled.
    @return: NA.
    """   
    def getStd(self):
        self["stdImageFile"]=self["RegMainDir"]+"/stdImage.mhd"
        for cnt in range(0,self.__sampleNum):
            self["defFieldDir"]=self["RegMainDir"]+"/NonRigid/Transformix"+str(cnt)
            self["nonRigRegDir"]=self["RegMainDir"]+"/NonRigid/Elastix"+str(cnt)
            self.getDeformationField()
        cmd=self["prePceCommands"]
        cmd+=self["PCE_Exe"]+" -rootDir "+self["RegMainDir"]+" -verbose -uncertainty 1_2-1-2-all"+" -sobol "+"-polOrderFile "+" -outDir "+self["RegMainDir"]+" -settingsFile "+self["PCE_ModelSetRunFile"]+" -runPCE "
        cmd+=self["postPceCommands"]
        os.system(cmd)
        for cnt in range(0,self.__sampleNum):
            self["defFieldDir"]=self["RegMainDir"]+"/NonRigid/Transformix"+str(cnt)
            shutil.rmtree(self["defFieldDir"])
    
    """
    @brief: Loads parameters to be analyzed.
    @param: file File name to load.
    @return: NA.
    """    
    def loadParamVals(self, file=""):
        if file=="":
            file=self["resultsRootDir"]+"/ParamVals.txt"
        if not os.path.isfile(file):
            assert("there is no file with the given name")   
        fl=open(file,"r")
        ln=fl.readlines()
        fl.close()
        self.__paramsToAnalyze=[]
        for it in ln:
            if it=="Param\n":
                self.__paramsToAnalyze+=[Param()]
            elif it.count("Name"):
                self.__paramsToAnalyze[-1:][0].setName(it[len("Name")+1:-1])
            elif it.count("Dist"):
                self.__paramsToAnalyze[-1:][0].setDist(it[len("Dist")+1:-1])
            elif it.count("Mean"):
                self.__paramsToAnalyze[-1:][0].setMean(it[len("Mean")+1:-1])
            elif it.count("Std"):
                self.__paramsToAnalyze[-1:][0].setStd(it[len("Std")+1:-1])
            elif it.count("HighBnd"):
                self.__paramsToAnalyze[-1:][0].setHighBnd(it[len("HighBnd")+1:-1])
            elif it.count("LowBnd"):
                self.__paramsToAnalyze[-1:][0].setLowBnd(it[len("LowBnd")+1:-1])
            elif it.count("Size"):
                continue
            elif not it=="\n":
                self.__paramsToAnalyze[-1:][0].addRandVal(it)
                continue
    
    """
    @brief: Saves parameters to be analyzed.
    @param: file File name to save.
    @return: NA.
    """
    def saveParamVals(self, file=""):
        if file=="":
            dr=self["resultsRootDir"]
            if not os.path.isdir(dr):
                os.makedirs(dr)
            file=dr+"/ParamVals.txt"
        fl=open(file,"w")
        for it in self.__paramsToAnalyze:
            fl.writelines("Param\n")
            fl.writelines("Name "+it.getName()+"\n")
            fl.writelines("Dist "+it.getDist()+"\n")
            fl.writelines("Mean "+str(it.getMean())+"\n")
            fl.writelines("Std "+str(it.getStd())+"\n")
            fl.writelines("HighBnd "+str(it.getHighBnd())+"\n")
            fl.writelines("HighBnd "+str(it.getLowBnd())+"\n")
            fl.writelines("Size "+str(it.getSize())+"\n")
            vals=it.getRandVal()
            for i in vals:
                fl.writelines(str(i)+"\n")
            fl.writelines("\n")
        fl.close()
    
    """
    @brief: Used to generate settings file for PCE executable as per PCE 
            settings.
    @return: NA.
    """
    def generatePceParamFile(self):
        ln="{\n"
        ln+="\"pol_order\" : \""+str(self.getPolOrder())+"\",\n"
        ln+="\"grid_level\" : \""+str(self.getGridLevel())+"\",\n"
        
        ln+="\"quadrature_type\" : ["
        quadType=self.getQuadratureType()
        for ind,it in enumerate(quadType):
            if not ind==0:
                ln+=","
            ln+="\""+it+"\""
        ln+="],\n"
            
        polType=self.getPolType()
        ln+="\"pol_type\" : ["
        for ind,it in enumerate(polType):
            if not ind==0:
                ln+=","
            ln+="\""+it+"\""
        ln+="],\n"
        
        ln+="\"grid_type\" : \""+str(self.getGridType())+"\",\n"
        ln+="\"trim\" : \""+str(self.getTrim())+"\",\n"
        ln+="\"remove_small_elements\" : \""+str(self.getRemoveSmallElements())+"\",\n"
        ln+="\"small_element_threshold\" : \""+str(self.getSmallElementThresh())+"\",\n"
        stdDev=self.getStdDevs()
        ln+="\"std_devs\" : ["
        for ind,it in enumerate(stdDev):
            if not ind==0:
                ln+=","
            ln+="\""+str(it)+"\""
        ln+="]\n}"
        fl=open(self["PCE_ModelSetRunFile"],"w")
        ln=fl.writelines(ln)
        fl.close() 
    
    """
    @brief: Used to generate instance settings file for PCE executable.
    @return: NA.
    """
    def generatePceParamFileFromInstance(self):
        fl=open(self["PceSetInstanceFile"],"r")
        ln=fl.readlines()
        fl.close()
        for cnt in range(0,len(ln)):
            if ln[cnt].count("quadrature_type")>0:
                ln[cnt]="\"quadrature_type\" : ["
                for ind,it in enumerate(self.__paramsToAnalyze):
                    if not ind==0:
                        ln[cnt]+=","
                    ln[cnt]+="\"gauss-"+self.__getPolType(it.getDist())+"\""
                ln[cnt]+="],\n"
            if ln[cnt].count("std_devs")>0:
                ln[cnt]="\"std_devs\" : ["
                for ind,it in enumerate(self.__paramsToAnalyze):
                    if not ind==0:
                        ln[cnt]+=","
                    ln[cnt]+="\""+str(it.getStd())+"\""
                ln[cnt]+="],\n" 
        fl=open(self["PCE_ModelSetRunFile"],"w")
        ln=fl.writelines(ln)
        fl.close()            
    
    """
    @brief: Used to generate weights file from PCE executable for registration sampling locations .
    @return: NA.
    """    
    def generateWeightFile(self):
        cmd=self["prePceCommands"]
        cmd+=self["PCE_Exe"]+" -settingsFile "+self["PCE_ModelSetRunFile"]+" -writePceWeights "+self["Pce_WeightFile"]
        cmd+=self["postPceCommands"]
        os.system(cmd)
    
    """
    @brief: Runs rigid registration.
    @return: NA.
    """ 
    def runRig(self):
        self["rigRegDir"]=self["RegMainDir"]+"/Rigid"
        if not os.path.exists(self["rigRegDir"]):
            os.makedirs(self["rigRegDir"])
        self.rigidElasRun()
    
    """
    @brief: Runs nonrigid registration.
    @return: NA.
    """ 
    def runNonRigSingle(self,ind):
        self["nonRigRegDir"]=self["RegMainDir"]+"/NonRigid/Elastix"+str(ind)
        paramDict={}
        elasParamDict={}
        for it in self.__paramsToAnalyze:
            paramDict.update({it.getName():it.getVals()[ind]})
            registrationParams=it["registrationParams"]
            for it2 in registrationParams:
                elasParamDict.update({it2:registrationParams[it2]})
        self.nonRigidElasRun(paramDict,elasParamDict)
    
    """
    @brief: Loads parameter values from a file with name embedded in 
            environment settings.
    @return: NA.
    """            
    def loadWeightFromFile(self):
        fl=open(self["Pce_WeightFile"],"r")
        ln=fl.readlines()
        fl.close()
        self.__sampleNum=int(ln[0])
        weights=[]
        for ind in range(0,self.__sampleNum):
            weights+=[ln[ind+1].split(",")]
        weights=list(map(list, zip(*weights)))
        
        for ind,it in enumerate(self.__paramsToAnalyze):
            it.resetVal()
            for ind2 in range(0,self.__sampleNum):
                it.addVal(float(weights[ind][ind2])+it.getMean())
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
        self.__weightsLs=self.__paramValTransFunc(self.__weightsLs)
      
    """
    @brief: Returns polynomial type of distributions.
    @param: dist Distribution.
    @return: Polynomial type.
    """
    def __getPolType(self,dist):
        if dist=="gauss":
            return "hermite"
        elif dist=="exponential":
            return "laguerre"
        elif self.__dist=="uniform":
            return "legendre"
        else:
            return ""
        
    """
    @brief: Used to add a new parameter to analyze.
    @param: param Parameter to be added.
    @return: NA.
    """
    def addParam(self,param):
        self.__paramsToAnalyze+=[param]
    
    """
    @brief: Returns parameters to be analyzed.
    @return: Parameters to be analyzed.
    """
    def getParams(self):
        return self.__paramsToAnalyze
    
    """
    @brief: Sets polynomial order.
    @param: order Polynomial order.
    @return: NA.
    """
    def setPolOrder(self,order):
        self.__polOrd=order
    
    """
    @brief: Sets grid level.
    @param: level Grid level.
    @return: NA.
    """
    def setGridLevel(self,level):
        self.__gridLevel=level
    
    """
    @brief: Sets quadrature type.
    @param: quadType Quadrature type.
    @return: NA.
    """
    def setQuadratureType(self,quadType):
        self.__quadratureType=quadType
    
    """
    @brief: Sets grid type.
    @param: typ Grid type.
    @return: NA.
    """
    def setGridType(self,typ):
        self.__gridType=typ
    
    """
    @brief: Sets trim value.
    @param: trm Trim value.
    @return: NA.
    """
    def setTrim(self,trm):
        self.__trim=trm
    
    """
    @brief: Sets remove small elements token in the PCE settings.
    @param: rem Token for removal.
    @return: NA.
    """
    def setRemoveSmallElements(self,rem):
        self.__removeSmallElements=rem
    
    """
    @brief: Sets threshold for small elements token in the PCE settings.
    @param: thresh Threshold value.
    @return: NA.
    """
    def setSmallElementThresh(self,thresh):
        self.__smallElementThresh=thresh
    
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
        quadType=[]
        polType=self.getPolType()
        for it in polType:
            quadType+=[self.__quadratureType+"-"+it]
        return quadType
    
    """
    @brief: Returns polynomial types of the parameter to be analyzed.
    @return: Polynomial types of the parameter to be analyzed.
    """    
    def getPolType(self):
        polType=[]
        for it in self.__paramsToAnalyze:
            polType+=[self.__getPolType(it.getDist())]
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
        stdDevs=[]
        for it in self.__paramsToAnalyze:
            stdDevs+=[str(it.getStd())]
        return stdDevs
    
    """
    @brief: Sets cluster waiting function.
    @param: waitFunc Waiting function.
    @return: NA.
    """   
    def setClusterWaitFunc(self,waitFunc):
        self.__clusterWaitFunc=waitFunc
        
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
    def setVerbose(self,verb=False):
        self.__verbose=verb
    
    """
    @brief: Sets a function mapping values of the parameter.
            this funtion is instantiated by a lambda function returning back 
            its input.
    @param: func A function to map the parameter values.
    @return: NA.
    """
    def setParamValTransFunc(self,func):
        self.__paramValTransFunc=func
    
    """
    @brief: Sets an internal token for loading parameters from previous run.
    @param: fromPrevious Binary value to set the internal token.
    @return: NA.
    """
    def loadParamsFromPreviousRun(self,fromPrevious=False):
        self.__loadFrompreviousRun=fromPrevious  
