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

import os
    
selfPath=os.path.dirname(os.path.realpath(__file__))
oneUpperPath=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

class MatlabExeCompiler(object):
    
    def __init__(self):
        self.__cmdCompile="mcc"
        self.__dict={}
        self.__dirMatlab=oneUpperPath+"/MatlabScripts"
        self.__verbose=True
        
    
    def __getitem__(self,key):
        try:
            return self.__dict[key]
        except:
            return ""
        
    def __setitem__(self,key,val):
        try:
            self.__dict.update({key:val})
        except:
            return
        
    def setMatlabDir(self,dr):
        self.__dirMatlab=dr
        
    def compileMatlabExe(self):
        dirList=self.getAllChildDirs(self.__dirMatlab)
        print(dirList)
        for ind in dirList:
            self.__cmdCompile+=" -a "+ind
        
        self.__cmdCompile+=" -m "+self.__dirMatlab+ "/pceExe.m"
        self.__cmdCompile=self["preCommands"]+self.__cmdCompile+self["postCommands"]
        if not (os.path.isfile(self.__dirMatlab+ "/pceExe")):
            if self.__verbose:
                print("Compiling Matlab Executable.")
            os.chdir(self.__dirMatlab)
            os.system(self.__cmdCompile)
            os.chdir(oneUpperPath)
            if self.__verbose:
                print("Compilation finished.")
            
    def getAllChildDirs(self,mainDir):
        ls=[]
        self.__Dirs(mainDir,ls)
        return ls
    
    def __Dirs(self,mainDir,ls):
        dirContents=os.listdir(mainDir)
        for ind in dirContents:
            if os.path.isdir(mainDir+"/"+ind):
                ls+=[mainDir+"/"+ind]
                self.__Dirs(mainDir+"/"+ind,ls)
    
    def isVerbose(self,verb):
        self.__verbose=verb
          

    