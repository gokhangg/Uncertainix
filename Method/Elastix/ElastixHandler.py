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

import re, shutil, os
import sys

if sys.version_info[0] == 3:
    import subprocess
    exeGetOutput = subprocess.getoutput
else:
    import commands
    exeGetOutput = commands.getoutput
    

class ElastixParamC(Base):
    
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


class Elastix(MethodB):
    __WaitFunction = lambda :0
    
    def __init__(self):
        pass
    
    def SetParamSettings(self, settings):
        self.__settings = settings
        
    def SetDataset(self, dataset):
        self.__dataset = dataset
    
    def SetParamVals(self, paramsAndVals):
        self.__paramsAndVals = paramsAndVals
    
    def SetEnvironment(self, env):
        self.__environment = env
        if "waitFunction" in env:
            self.__WaitFunction = env["waitFunction"]
    
    def Run(self, abortRigidIfExist = False):
        self.__finished = False
        self.__RunRigidElas(abortRigidIfExist, self.__dataset["rigidElasDict"])
        self.__WaitFunction()
        for dataSetIndex in range(len(self.__paramsAndVals)):
            outDir = self.__GetNonRigidDir(dataSetIndex)
            self.__CreateDir(outDir)
            self.__CreateNonRigidParamFile(dataSetIndex)
            paramFile = ElastixParamC(self.__GetNonRigidDir(dataSetIndex) + "/parameterFile.txt")
            for param in self.__paramsAndVals["parameters"]:
                ChangeParameterValue(self, param["name"], param["value"])
            self.__RunNonrigidElas(dataSetIndex, self.__dataset["nonRigElastixDict"])
        self.__WaitFunction()
        self.__GetDeformationField(self, index)
            self.__WaitFunction()
        self.__finished = True

    def IsFinished(self):
        return self.__finished
    
    def GetResultWithIndex(self):
        pass
    
    def __RunRigidElas(self, abortIfExist = False, elasDict = dict()):
        if abortIfExist and os.path.exists(self.__environment["rigOutDir"] + "/TransformParameters.0.txt"):
            return
        elasDict.update({"elastixExe":self.__environment["elastixExe"]})
        elasDict.update({"-f":self.__dataset["fixedIm"]})
        elasDict.update({"-m":self.__dataset["movingIm"]})
        elasDict.update({"-p":self.__environment["rigidParam"]})
        elasDict.update({"-out":self.__environment["rigOutDir"]})
        self.__RunElasTrans(self.__environment["elastixExe"], elasDict)
        
    def __RunNonrigidElas(self, index, elasDict = dict()):
        elasDict.update({"-f":self.__dataset["fixedIm"]})
        elasDict.update({"-m":self.__dataset["movingIm"]})
        elasDict.update({"-out":self.__GetNonRigidDir(index))
        elasDict.update({"-p":self.__GetNonRigidDir(index) + "/parameterFile.txt"})
        elasDict.update({"-t0":self.__environment["rigOutDir"] + "/TransformParameters.0.txt"})
        self.__RunElasTrans(self.__environment["elastixExe"], elasDict)
        
    """
        @brief: Runs transformix to get deformation field 
    """
    def __GetDeformationField(self, index, transDict = dict()):
        dir_ = self.__GetNonRigidDir(index)
        transDict["-tp"] = dir_ + "/TransformParameters.0.txt"
        assert os.path.isfile(transDict["-tp"]), "there is no transform parameter file to extract def field"
        transDict["-out"] = self.__environment["nonrigOutMainDir"] + "/Trans{0:d}".format(ind)
        transDict["-def"] = "all"
        self.__CreateDir(transDict["-out"])
        self.__RunElasTrans(self.__environment["transformixExe"], transDict)
            
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
        
    def __GetNonRigidDir(self, ind):
        return self.__environment["nonrigOutMainDir"] + "/Elas{0:d}".format(ind)
    
    def __CreateNonRigidParamFile(self, ind):
        dirToSave = self.__GetNonRigidDir(ind)
        shutil.copy(self.__environment["nonrigidParam"], dirToSave + "/paramFile.txt")
        
    def __CreateDir(self, dir_):
        if not os.path.exists(dir_):
            os.makedirs(dir_) 