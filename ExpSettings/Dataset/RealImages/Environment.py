# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 17:02:31 2020

@author: ghngu
"""
from ExpSettings.EnvBase import EnvBase

import sys, time, os
_selfPath = os.path.dirname(__file__)

if sys.version_info[0] == 3:
    import subprocess
    exeGetOutput = subprocess.getoutput
else:
    import commands
    exeGetOutput = commands.getoutput

"""
@brief: It just waits till end of all 
        jobs of the user.
@Note:  Experiments were executed on the BIGR cluster facility and this 
        method is wait function for this cluster. Therefore, for a different
        cluster this method should be revisited and modified.
"""
def WaitCluster():
    Qstat = exeGetOutput("qstat ")
    cnt = 0
    while Qstat.count("\n") > 1:
        Qstat = exeGetOutput("qstat ")
        if not cnt == Qstat.count("\n"):
            cnt = Qstat.count("\n")
            print("Remaining Task ", cnt - 1)
        time.sleep(10)  


class Environment(EnvBase):
    
    def __init__(self, rootDirectory):
        self.__dictionary = {}
        #Root Dir where the results to be saved
        self["rootDir"] = rootDirectory
        self["experimentsRootDir"] = self["rootDir"] + "/ExperimentResults/RealImages"
        #Rootdir where registration results to be saved
        self["WaitFunction"] = WaitCluster
        
        
        #Settings file for PCE execution model
        self["pceModelSetRunFile"] = _selfPath + "/PCE_Settings.json"
        #Elastix executable 
        self["elastixExe"] = "/tools/elastix/bin/bin/elastix"
        #Transformix executable
        self["transformixExe"] = "/tools/elastix/bin/bin/transformix"
    
    def GetEnvironmentDict(self, el = {}):
        return self.__dictionary
        
    def __getitem__(self, key):
        if key in self.__dictionary:
            return self.__dictionary[key]
        return None
    
    def __setitem__(self, key, val):
        self.__dictionary.update({key : val})