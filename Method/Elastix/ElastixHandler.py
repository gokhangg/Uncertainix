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

from Method.MethodB import MethodB as Base
from ItkHandler import ItkHandler

import re, shutil, os
import sys

if sys.version_info[0] == 3:
    import subprocess
    exeGetOutput = subprocess.getoutput
else:
    import commands
    exeGetOutput = commands.getoutput
    

class ElastixParamFileModifier():
    
    def __init__(self, file, verbose = False):
        self.__file = file
        self.__verbose = verbose
               
    """
        @brief: Replaces a parameter in an Elastix parameter file.
        @param: fileName Parameter file to be modified.
        @param: param Parameter which is looked for.
        @param: value New value for the parameter.
    """
    def ChangeParameterValue(self, param, value):
        Res1 = self.__FindLines(self.__file, param + " ")
        assert Res1[0] == 1, ("Maldefinition of the parameter")
        self.__ReplaceLine(self.__file, Res1[1][0][0], "(" + param + " " + str(value) + ")\n")
        if self.__verbose:
            print("Maldefinition of the parameter")
            
    """
        @brief: Finds a keyword(s) in a text file, this function is intended
                for modification of Elastix parameter files.
        @param: fileName Name of the file where a specfic keyword(s) is sought.
        @param: key A specfic keyword(s) which is sought.
        @return: found Number of lines where the sought keyword(s) is found, 
                lines Found lines and their indexes. 
    """
    def __FindLines(self, fileName, key):
        pattern = re.compile(key)
        found = 0
        lines = {}
        #line by line search on the file and assigning corresponding numberline
        for i, line in enumerate(open(fileName)):
            for match in re.finditer(pattern, line):
                lines[found] = [i, line]
                found += 1
        return [found, lines]
    
    """
        @brief: Replaces a line in a text.
        @param: fileName  Name of the text file to be modified.
        @param: lineNum Number of the line to be replaced.
        @param: key A string which is to replace the line.
    """
    def __ReplaceLine(self, fileName, lineNum, key):
        lines = open(fileName, 'r').readlines()
        lines[lineNum] = key
        out = open(fileName, 'w')
        out.writelines(lines)
        out.close()    


class Elastix(Base):
    __WaitFunction = lambda :0
    
    def __init__(self):
        pass
    
    def SetExperSettings(self, settings):
        self.__experimentSettings = settings
        
        self.__environment = settings.GetEnvironment()
        if "WaitFunction" in self.__environment:
            self.__WaitFunction = self.__environment["WaitFunction"] 
        
    def Run(self, datasetIndex, abortRigidIfExist = False):
        self.__finished = False
        
        self.__UpdateEnvironmentDict(datasetIndex)
        
        """Run Rigid registration first to init the registrations"""
        self.__RunRigidElas(abortRigidIfExist)
        self.__WaitFunction()
        
        """Since each nonrigid registration is done as per the parameter values,
           we take parameter value gorups as index.         
        """
        expSize = self.__experimentSettings.GetNonrigCount(datasetIndex)
        for expInd in range(expSize):
            expDir = self.__envDict["NonrigRegDirs"][expInd]
            self.__CreateDir(expDir)
            nonrigidParamFile = self.__CreateNonRigidParamFile(expInd)
            
            """Non rigid parameter file is generated in its folder.
               We are changing the paremeter values used in the experiment. 
            """
            paramValues = self.__paramSettings.GetParamVals()[expInd]
            paramFile = ElastixParamFileModifier(nonrigidParamFile)
            """We are changing values in the parameter file as per parameters."""
            for ind, param in enumerate(self.__paramsAndVals.GetParamNames()):
                paramFile.ChangeParameterValue(self, param, paramValues[ind])
            
            """The last point is to run the nonrigid registration"""
            self.__RunNonrigidElas(datasetIndex, expInd)
        """All non rigid registrations perhaps are need to be finished
           So waiting here if the wait functio is set.
        """   
        self.__WaitFunction()
        self.__finished = True
        
    def IsFinished(self):
        return self.__finished
    
    def GetResultWithIndex(self, index):
        pass
    
    def __UpdateEnvironmentDict(self, datasetIndex):
        exprRoot = self.__environment["ExperimentsRootDir"]
        expSize = self.__experimentSettings.GetExperimentSize()
        
        envDict = {}
        envDict.update({"ElastixExe":self.__environment["ElastixExe"]})
        envDict.update({"TransformixExe":self.__environment["TransformixExe"]})
        envDict.update({"RigidRegDir":exprRoot + "/Dataset{0:d}/Rig".format(datasetIndex)})
        
        nonrigDirs = [exprRoot + "/Dataset{0:d}/Nonrig/Elas{1:d}".format(datasetIndex, ind) for ind in range(expSize)]
        envDict.update({"NonrigidRegDirs":nonrigDirs})
        transDirs = [exprRoot + "/Dataset{0:d}/Nonrig/Trans{1:d}".format(datasetIndex, ind) for ind in range(expSize)]
        envDict.update({"TransDirs":transDirs})
        
        envDict.update({"RigidParameterFile": self.__environment["RigidParameterFile"]})
        envDict.update({"NonrigidParameterFile": self.__environment["NonrigidParameterFile"]})
        self.__envDict = envDict
       
    
    def __RunRigidElas(self, datasetIndex, abortIfExist = False):
        if abortIfExist and os.path.exists(self.__environment["rigOutDir"] + "/TransformParameters.0.txt"):
            return
        elasDict = self.__experimentSettings.GetRigidElastixSettings(datasetIndex)
        elasDict.update({"-p":self.__envDict["RigidParameterFile"]})
        elasDict.update({"-out":self.__envDict["RigRegDir"]})
        self.__RunElasTrans(self.__envDict["ElastixExe"], elasDict)
        
    def __RunNonrigidElas(self, datasetIndex, nonrigidExpIndex):
        elasDict = self.__experimentSettings.GetNonrigidElastixSettings(datasetIndex, nonrigidExpIndex)
        expDir = self.__envDict["NonrigidRegDirs"][nonrigidExpIndex]
        elasDict.update({"-out":expDir})
        elasDict.update({"-p":expDir + "/parameterFile.txt"})
        elasDict.update({"-t0":self.__environment["RigRegDir"] + "/TransformParameters.0.txt"})
        self.__RunElasTrans(self.__envDict["ElastixExe"], elasDict)
        
        
    """
        @brief: Runs transformix to get deformation field 
    """
    def __GetDeformationField(self, datasetIndex, nonrigidExpIndex, transDict = dict()):
        assert self.IsFinished, "Nonrigid registration have not finished."
        
        transDict = self.__paramSettings.GetNonrigTransformixSettings(datasetIndex, nonrigidExpIndex)
        
        expDir = self.__envDict["NonrigidRegDirs"][nonrigidExpIndex]
        transDict["-tp"] = expDir + "/TransformParameters.0.txt"
        assert os.path.isfile(transDict["-tp"]), "there is no transform parameter file to extract def field"
        
        transDict["-out"] = self.__envDict["TransDirs"][nonrigidExpIndex]
        transDict["-def"] = "all"
        self.__CreateDir(transDict["-out"])
        self.__RunElasTrans(self.__envDict["transformixExe"], transDict)
        
        return nonrigidExpIndex, ItkHandler.LoadItkImage(transDict["-out"] + "/result.mhd")
            
    """
        @brief:  Runs elastix.
        @return: Returns executable response.
    """
    def __RunElasTrans(self, cmd, _dict):
        cmd += " "
        self.__CreateDir(_dict["out"])
        for key in _dict:
            cmd += key + " " + _dict[key] + " "
        return exeGetOutput(cmd)   
        
    
    def __CreateNonRigidParamFile(self, ind):
        dirToSave = self.__envDict["NonrigRegDirs"][ind]
        outFile = dirToSave + "/nonRigParamFile.txt"
        shutil.copy(self.__envDict["NonrigidParameterFile"], outFile)
        return outFile
        
    def __CreateDir(self, dir_):
        if not os.path.exists(dir_):
            os.makedirs(dir_) 