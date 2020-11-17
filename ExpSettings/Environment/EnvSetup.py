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

import os, ast

class Environment(object):
    __verbose = False

    def __init__(self):
        self.selfPath = os.path.dirname(__file__)
        self.envLogFile = os.path.splitext(__file__)[0] + ".json"
        self.__envLogs = self.envEnvDictInstance()
    
    """
    @brief: Reads the environmental settings file and returns as a dictionary.
    """
    def envLoadSettingsFromFile(self):
        if not os.path.isfile(self.envLogFile):
            """Env log file is not present, return void string"""
            if self.__verbose:
                print("Env log file is not present, instance dictionary loaded.\n")
            self.__envLogs = self.envEnvDictInstance()
        else:
            self.__envLogs = self.__envDictFileReader(self.envLogFile)
    
    """
    @brief: Saves the environmental dictionary file.
    """
    def envSaveEnvDict(self):
        self.__envDictFileWriter(self.envLogFile, self.__envLogs)
        if self.__verbose:
            print("The dictionary has been saved")
    
    """
    @brief: Saves a key and its value to PCE environmental setting file.
    """
    def envSaveEnvDictKey(self, key, val):
        if not os.path.isfile(self.envLogFile):
            self.__envDictFileWriter(self.envLogFile, {key:val})
        else:
            dictExt = self.__envDictFileReader(self.envLogFile)
            dictExt[key] = val
            self.__envDictFileWriter(self.envLogFile, dictExt)
        if self.__verbose:
            print("The key has been saved")
    
    """
    @brief: Deletes a key and its value from PCE environmental setting file.
    @param: key A key to be deleted from the environment dictionary and file.
    """
    def envDeleteEnvDictKey(self, key):
        if not os.path.isfile(self.envLogFile):
            if self.__verbose:
                print("There is no global env. setup file")
        else:
            previousDict = self.__envDictFileReader(self.envLogFile)
            if key in previousDict:
                previousDict.pop(key)
                self.__envDictFileWriter(self.envLogFile, previousDict)
                if self.__verbose:
                    print("The key has been deleted global env setup file")
                self.__envLogs = previousDict
            else:
                if self.__verbose:
                    print("There is no such a key to be deleted")
    
    """
    @brief: Deletes environment log file.
    """
    def envDeleteEnvFile(self):
        os.remove(self.envLogFile)
        
    """
    @brief: Reads a saved dictionary from a file.
    @param: fl Name of the file where a dict file saved.
    """
    def __envDictFileReader(self, fl):
        if os.path.isfile(fl) != True:
            return {}
        flR = open(fl, 'r')
        text = flR.read()
        flR.close() 
        return ast.literal_eval(text)
    
    """
    @brief: Writes a dictionary to a File.
    @param: fl Name of the file where a dict file is saved.
    @param: dct Dictionary to be saved.
    """
    def __envDictFileWriter(self, fl, dct):
        text = str(dct)
        text2 = ""
        for i in range(0, len(text)):
            if text[i] == "'":
                text2 += "\""
            else:
                text2 += text[i]
        flW = open(fl, 'w')
        flW.write(str(text2))
        flW.close()
        
    
    """
    @brief: Sets a key in the environmental dictionary.
    @param: key A key to be added to the dictionary.
    @param: val Value of the key to be added to the dictionary.
    """
    def envSetEnvDictKey(self, key, val):
        self.__envLogs.update({key:val})
       
    """
    @brief: Gets environmental dictionary.
    """
    def envGetEnvDict(self):
        return self.__envLogs
   
    """
    @brief: Returns an instance of environmental dictionary.
    """
    def envEnvDictInstance(self):
        #Self file 
        envLogDict = {"EnvLogFile":self.envLogFile}
        #Root Dir where the results to be saved
        envLogDict.update({"ResultsRootDir":""})
        #Path of PCE executable
        envLogDict.update({"PCE_ExePath":""})
        #Name of the PCE executable
        envLogDict.update({"PCE_ExeName":""})
        #PCE executable
        envLogDict.update({"PCE_Exe":""})
        #Example settings for PCE execution model
        envLogDict.update({"PCE_ModelSetExmFile":""})
        #Settings file for PCE execution model
        envLogDict.update({"PCE_ModelSetRunFile":""})
        #Elastix executable 
        envLogDict.update({"ElastixExe":""})
        #Transformix executable
        envLogDict.update({"TransformixExe":""})
        #Rootdir where registration results to be saved
        envLogDict.update({"RegistRootDir":""})
        #Path of Intra dataset
        envLogDict.update({"FixedDatasetPath":""})
        #Path of Pre dataset
        envLogDict.update({"MovingDatasetPath":""})
        #Path of segmentation dataset
        envLogDict.update({"SegDatasetPath":""})
        #Path of mask dataset
        envLogDict.update({"MaskDatasetPath":""})
        #Rigid registration parameter file
        envLogDict.update({"RigidParaTemplate":""})
        #Nonrigid registration parameter file
        envLogDict.update({"NonRigidParaTemplate":""})
        return envLogDict
    
    """
    @brief: Assigns value for verbose execution.
    """
    def isVerbose(self, verb):
        self.__verbose = verb
        
    def __getitem__(self, key):
        try:
            return self.__envLogs[key]
        except:
            return ""
        
    def __setitem__(self, key, val):
        self.__envLogs.update({key:val})
        
    def __str__(self):
        return "Environment setup class, used to manage the experimental setup.\n"