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

import os,re,shutil

import sys
if sys.version_info[0]==3:
    import subprocess
    exeGetOutput=subprocess.getoutput
else:
    import commands
    exeGetOutput=commands.getoutput

from EnvSetup import*

class Elastix(Environment):
    __verbose=False
    __elastixOnCluster=False
    __transformixOnCluster=False
    __elastixClusterCmd=""
    __transformixClusterCmd=""
    
    def __init__(self):
        super(Elastix, self).__init__()
        self.__elastixDict=self.getElastixParamDictInstance()
        self.__transformixDict=self.getTransformixParamDictInstance()
        
    """
        @brief: Assigns value for verbose execution
    """
    def isVerbose(self,verb):
        self.__verbose=verb
        
    """
        @brief: If you use the code on multiple node computer cluster 
                assign an appropriate cmd.
        @param: cmd an appropriate cluster command.
    """
    def elastixSetClusterCommand(self,cmd):
        self.__elastixClusterCmd=cmd
    
    """
        @brief: If you use the code on multiple node computer cluster assign
                this method with True after assignment cluster command.
        @param: onCluster Selection of execution on cluster.
    """
    def elastixOnCluster(self,onCluster=False):
        if len(self.__elastixClusterCmd)>0:
            self.__elastixOnCluster=onCluster
        else:
            self.__elastixOnCluster=False

    """
        @brief: If you use the code on multiple node computer cluster assign
                appropriate cmd.
        @param: cmd an appropriate cluster command.
    """
    def transformixSetClusterCommand(self,cmd):
        self.__transformixClusterCmd=cmd
    
    """
        @brief: If you use the code on multiple node computer cluster assign
                pass this method with True after assignment cluster command.
        @param: onCluster Selection of execution on cluster.
    """
    def transformixOnCluster(self,onCluster=False):
        if len(self.__transformixClusterCmd)>0:
            self.__transformixOnCluster=onCluster
        else:
            self.__transformixOnCluster=False
            
    """
        @brief: Finds a keyword(s) in a text file, this function is intended
                for modification of Elastix parameter files.
        @param: fileName Name of the file where a specfic keyword(s) is sought.
        @param: key A specfic keyword(s) which is sought.
        @return: found Number of lines where the sought keyword(s) is found, 
                lines Found lines and their indexes. 
    """
    def find_lines(self,fileName,key): 
        pattern = re.compile(key)
        found=0
        lines={}
        #line by line search on the file and assigning corresponding numberline
        for i, line in enumerate(open(fileName)):
            for match in re.finditer(pattern, line):
                lines[found]=[i,line]        
                found+=1
        return [found,lines]
    
    """
        @brief: Replaces a line in a text.
        @param: fileName  Name of the text file to be modified.
        @param: lineNum Number of the line to be replaced.
        @param: key A string which is to replace the line.
    """
    def replace_line(self,fileName, lineNum, key):
        lines = open(fileName, 'r').readlines()
        lines[lineNum] = key
        out = open(fileName, 'w')
        out.writelines(lines)
        out.close()

    """
        @brief: Replaces a parameter in an Elastix parameter file.
        @param: fileName Parameter file to be modified.
        @param: param Parameter which is looked for.
        @param: value New value for the parameter.
    """
    def change_parameter_file(self,fileName,param,value):
        Res1=self.find_lines(fileName,param+" ")
        if Res1[0]>1:
            if self.__verbose:
                print("Maldefinition of the parameter")
            return 0
        self.replace_line(fileName,Res1[1][0][0],"("+param+" "+str(value)+")\n")
        if self.__verbose:
            print("Parameter file modified")
            
    """
        @brief:  Runs elastix.
        @return: Returns executable response.
    """
    def runElastix(self):
        cmd=self["elastixExe"]+" "
        for key in self.__elastixDict:
            if not self.__elastixDict[key]=="":
                if key=="-out":
                    if not os.path.exists(self.__elastixDict[key]):
                        os.makedirs(self.__elastixDict[key])
                cmd+=key+" "+self.__elastixDict[key]+" "
        if not self.__elastixOnCluster:
            os.system(cmd)
        else:
            return exeGetOutput(self.__elastixClusterCmd+" "+cmd)

    """
        @brief:  Runs transformix.
        @return: Returns executable response.
    """
    def runTransformix(self):
        Cmd=self["transformixExe"]+" "
        for Key in self.__transformixDict:
            if not self.__transformixDict[Key]=="":
                if Key=="-out":
                    if not os.path.exists(self.__transformixDict[Key]):
                        os.makedirs(self.__transformixDict[Key])
                Cmd+=Key+" "+self.__transformixDict[Key]+" "
        if not self.__transformixOnCluster:
            os.system(Cmd)
        else:
            return exeGetOutput(self.__transformixClusterCmd+" "+Cmd)
    
    """
        @brief: Returns instance for Elastix parameters.
    """
    def getElastixParamDictInstance(self):
        return {"-f":"","-m":"","-p":"","-t0":"","-out":""}
    
    """
        @brief: Returns instance for Transformix parameters.
    """
    def getTransformixParamDictInstance(self):
        return {"-in":"","-tp":"","-out":"","-def":""}
    
    """
        @brief: Returns current Elastix parameters.
    """
    def getElastixParamDict(self):
        return self.__elastixDict
    
    """
        @brief: Returns current Transformix parameters.
    """
    def getTransformixParamDict(self):
        return self.__transformixDict
    
    """
        @brief: Adds an Elastix parameter.
    """
    def addElastixParamDict(self,Key,Val):
        self.__elastixDict.update({Key:Val})
    
    """
        @brief: Adds a Transformix parameter.
    """
    def addTransformixParamDict(self,Key,Val):
        self.__transformixDict.update({Key:Val})
    
    """
        @brief: Sets Transformix parameters.
    """
    def setTransformixParamDict(self,dict_):
        self.__transformixDict=dict_
        
    """
        @brief: Sets Elastix parameters.
    """
    def setElastixParamDict(self,dict_):
        self.__elastixDict=dict_
        
    """
        @brief: Runs Elastix for rigid registration; used for initialization.
        @param: paramDict Elastix parameters to be changed in the Elastix 
                parameter file with the values provided.
        @return: self.runElastix() method return.
        @note:  This function to be modified for specific purposes.
    """
    def rigidElasRun(self,paramDict={},addElParam={}):
            self.__elastixDict=self.getElastixParamDictInstance()
            self.__elastixDict["-f"]=self["fixedIm"]
            self.__elastixDict["-m"]=self["movingIm"]
            self.__elastixDict["-out"]=self["rigRegDir"]
            if not os.path.exists(str(self.__elastixDict["-out"])):
                os.makedirs(str(self.__elastixDict["-out"]))
            self.__elastixDict["-p"]=self.__elastixDict["-out"]+"/NonRigidPara.txt"
            shutil.copyfile(self["rigidParaTemplate"], self.__elastixDict["-p"])
            self.__elastixDict.update(addElParam)
            for key in paramDict:
                self.change_parameter_file( self.__elastixDict["-p"],key,paramDict[key])
            return self.runElastix()
    
    """
        @brief: Runs elastix for nonrigid registration
        @param: paramDict Elastix parameters to be changed in the Elastix 
                parameter file with the values provided.
        @return: self.runElastix() method return.
        @note:  This function to be modified for specific purposes.
    """
    def nonRigidElasRun(self,paramDict={},addElParam={}):
            self.__elastixDict=self.getElastixParamDictInstance()
            self.__elastixDict["-f"]=self["fixedIm"]
            self.__elastixDict["-m"]=self["movingIm"]
            self.__elastixDict["-out"]=self["nonRigRegDir"]
            if not os.path.exists(str(self.__elastixDict["-out"])):
                os.makedirs(str(self.__elastixDict["-out"]))
            self.__elastixDict["-t0"]=self["rigRegDir"]+"/TransformParameters.0.txt"
            self.__elastixDict["-p"]=self.__elastixDict["-out"]+"/NonRigidPara.txt"
            shutil.copyfile(self["nonRigidParaTemplate"], self.__elastixDict["-p"])
            self.__elastixDict.update(addElParam)
            for key in paramDict:
                self.change_parameter_file( self.__elastixDict["-p"],key,paramDict[key])
            return self.runElastix()
        
    """
        @brief: Runs transformix to get deformation field 
    """
    def getDeformationField(self):
            self.__transformixDict=self.getTransformixParamDictInstance()
            self.__transformixDict["-tp"]=self["nonRigRegDir"]+"/TransformParameters.0.txt"
            if not os.path.isfile(self.__transformixDict["-tp"]):
                if self.__verbose:
                    print("there is no transform parameter file to extract def field")
                return
            self.__transformixDict["-out"]=self["defFieldDir"]
            self.__transformixDict["-def"]="all"
            self.runTransformix()
    
    """
        @brief: Runs transformix to deform an image 
    """
    def deformIm(self):
            self.__transformixDict=self.getTransformixParamDictInstance()
            self.__transformixDict["-tp"]=self["nonRigRegDir"]+"/TransformParameters.0.txt"
            if not os.path.isfile(self.__transformixDict["-tp"]):
                if self.__verbose:
                    print("there is no transform parameter file to extract def field")
                return
            self.__transformixDict["-out"]=self["imToDeformDir"]
            self.__transformixDict["-in"]=self["imToDeform"]
            self.runTransformix()
            