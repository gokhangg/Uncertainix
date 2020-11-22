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
from ItkHandler.ItkHandler import ItkHandler

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
    
    def SetMethodSettings(self, settings):
        self.__settings = settings
        
        envDict = self.__settings["environment"].GetEnvironmentDict()
        if "WaitFunction" in envDict:
            self.__WaitFunction = envDict["WaitFunction"] 
        
    def Run(self, datasetIndex, abortRigidIfExist = False):
        self.__finished = False
        self.__datasetIndex = datasetIndex
        self.__UpdateEnvironmentDict(datasetIndex)
        
        """Run Rigid registration first to init the registrations"""
        self.__CreateDir(self.__envDict["rigidRegDir"])
        self.__RunRigidElas(abortRigidIfExist)
        self.__WaitFunction()
        
        """Since each nonrigid registration is done as per the parameter values,
           we take parameter value gorups as index.         
        """
        parameters = self.__settings["parameters"]
        expSize = len(parameters[0].GetValues())
        for expInd in range(expSize):
            expDir = self.__envDict["nonrigidRegDirs"][expInd]
            self.__CreateDir(expDir)
            nonrigidParamFile = self.__CreateNonRigidParamFile(expInd)
            
            """Non rigid parameter file is generated in its folder.
               We are changing the paremeter values used in the experiment. 
            """
            paramFile = ElastixParamFileModifier(nonrigidParamFile)
            """We are changing values in the parameter file as per parameters."""
            for param in parameters:
                paramFile.ChangeParameterValue(param.GetName(), param.GetValues()[expInd])
            
            """The last point is to run the nonrigid registration"""
            self.__RunNonrigidElas(expInd, nonrigidParamFile)
        """All non rigid registrations perhaps are needed to be finished
           So waiting here if the wait functio is set.
        """   
        self.__WaitFunction()
        self.__finished = True
        
    def IsFinished(self):
        return self.__finished

    def GetResultsReady(self, indices):
        self.__GetDeformationFieldsReady(indices)
    
    def GetResultWithIndex(self, index):
        return self.__GetDeformationFieldAndRemoveFile(index)
    
    def __UpdateEnvironmentDict(self, datasetIndex):
        environment = self.__settings["environment"]
        
        exprRoot = environment["experimentsRootDir"]
        expSize = len(self.__settings["parameters"][0].GetValues())
        
        envDict = {}
        envDict.update({"elastixExe":environment["elastixExe"]})
        envDict.update({"transformixExe":environment["transformixExe"]})
        envDict.update({"rigidRegDir":exprRoot + "/Dataset{0:d}/Rig".format(datasetIndex)})
        
        nonrigDirs = [exprRoot + "/Dataset{0:d}/Nonrig/Elas{1:d}".format(datasetIndex, ind) for ind in range(expSize)]
        envDict.update({"nonrigidRegDirs":nonrigDirs})
        transDirs = [exprRoot + "/Dataset{0:d}/Nonrig/Trans{1:d}".format(datasetIndex, ind) for ind in range(expSize)]
        envDict.update({"transDirs":transDirs})
        
        parameterFiles = self.__settings["extension"]["parameterFiles"]
        envDict.update({"rigidParameterFile":  parameterFiles["rigidParameterFile"]})
        envDict.update({"nonrigidParameterFile":  parameterFiles["nonrigidParameterFile"]})
        self.__envDict = envDict
       
    
    def __RunRigidElas(self, abortIfExist = False):
        if abortIfExist and os.path.exists(self.__environment["rigOutDir"] + "/TransformParameters.0.txt"):
            return
        
        dataset = self.__settings["dataset"]
        
        elasDict = {"-f": dataset["fixedIm"]}
        elasDict.update({"-m": dataset["movingIm"]})
        elasDict.update({"-p":self.__envDict["rigidParameterFile"]})
        elasDict.update({"-out":self.__envDict["rigidRegDir"]})
        return self.__RunElasTrans(self.__envDict["elastixExe"], elasDict)
        
    def __RunNonrigidElas(self, nonrigidExpIndex, nonrigidParamFile):
        dataset = self.__settings["dataset"]
        extension = self.__settings["extension"]
        
        elasDict = extension["commandlineParameters"]
        elasDict.update({"-f": dataset["fixedIm"]})
        elasDict.update({"-m": dataset["movingIm"]})
        
        elasDict.update({"-out": self.__envDict["nonrigidRegDirs"][nonrigidExpIndex]})
        elasDict.update({"-p": nonrigidParamFile})
        elasDict.update({"-t0": self.__envDict["rigidRegDir"] + "/TransformParameters.0.txt"})
        self.__RunElasTrans(self.__envDict["elastixExe"], elasDict)
        
        
    """
        @brief: Runs transformix to get deformation field 
    """
    def __GetDeformationFieldReady(self, nonrigidExpIndex, transDict = dict()):
                
        expDir = self.__envDict["nonrigidRegDirs"][nonrigidExpIndex]
        transDict["-tp"] = expDir + "/TransformParameters.0.txt"
        assert os.path.isfile(transDict["-tp"]), "there is no transform parameter file to extract def field"
        
        transDict["-out"] = expDir
        transDict["-def"] = "all"
        self.__RunElasTrans(self.__envDict["transformixExe"], transDict)

    """
    @brief: Runs transformix to get deformation fields 
    """
    def __GetDeformationFieldsReady(self, nonrigidExpIndices, transDict = dict()):
        for ind in nonrigidExpIndices:
            self.__GetDeformationFieldReady(ind, transDict)

    """
        @brief: Runs transformix to get deformation field 
    """
    def __GetDeformationFieldAndRemoveFile(self, nonrigidExpIndex):              
        expDir = self.__envDict["nonrigidRegDirs"][nonrigidExpIndex]
        assert os.path.isfile(expDir + "/TransformParameters.0.txt"), "there is no transform parameter file to extract def field"
        itkIm = ItkHandler()
        itkIm.LoadImage(expDir + "/deformationField.mhd")
        os.remove(expDir + "/deformationField.mhd")
        os.remove(expDir + "/deformationField.raw")
        return nonrigidExpIndex, itkIm
            
    """
        @brief:  Runs elastix.
        @return: Returns executable response.
    """
    def __RunElasTrans(self, cmd, _dict):
        print(cmd, _dict)
        cmd += " "
        self.__CreateDir(_dict["-out"])
        for key in _dict:
            cmd += key + " " + _dict[key] + " "
        return print(exeGetOutput(cmd))
    
        
    
    def __CreateNonRigidParamFile(self, ind):
        dirToSave = self.__envDict["nonrigidRegDirs"][ind]
        outFile = dirToSave + "/nonRigParamFile.txt"
        shutil.copy(self.__envDict["nonrigidParameterFile"], outFile)
        return outFile
        
    def __CreateDir(self, dir_):
        if not os.path.exists(dir_):
            os.makedirs(dir_) 