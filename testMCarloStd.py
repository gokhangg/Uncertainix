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


import sys,time,os
import lib.Param as PR
import lib.MonteCarlo as MC
import DatasetsAndParameters.Dataset as Dataset

if sys.version_info[0]==3:
    import subprocess
    exeGetOutput=subprocess.getoutput
else:
    import commands
    exeGetOutput=commands.getoutput

SelfPath=os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0,"./lib")
sys.path.insert(0,"../lib")

"""
@brief: It just waits till end of all 
        jobs of the user.
@Note:  Experiments were executed on the BIGR cluster facility and this 
        method is wait function for this cluster. Therefore, for a different
        cluster this method should be revisiteda dn modified.
"""
def waitCluster():
    Qstat=exeGetOutput("qstat ")
    cnt=0
    while Qstat.count("\n")>1:
        Qstat=exeGetOutput("qstat ")
        if not cnt==Qstat.count("\n"):
            cnt=Qstat.count("\n")
            print("Remaining Task ",cnt-1)
        time.sleep(2)  


def setupEnvSimulatedData(el):
     #Root Dir where the results to be saved
    el["RootDir"]=SelfPath
    el["resultsRootDir"]=el["RootDir"]+"/ExpResults/MC"
    #Rootdir where registration results to be saved
    el["registRootDir"]=el["resultsRootDir"]
    #Path of Intra dataset
    el["fixedDatasetPath"]=el["RootDir"]+"/TestImages"
    #Path of Pre dataset
    el["movingDatasetPath"]=el["RootDir"]+"/TestImages"
    #Path of segmentation dataset
    el["segDatasetPath"]=el["RootDir"]+"/TestImages"

    #Rigid registration parameter file template
    el["rigidParaTemplate"]=el["RootDir"]+"/ParameterFiles/RigidparaPI.txt"
    #Nonrigid registration parameter file template
    el["nonRigidParaTemplate"]=el["RootDir"]+"/ParameterFiles/Nonrigidpara2ndStep.txt"
    #Example settings for PCE execution model
    el["PceSetInstanceFile"]=el["RootDir"]+"/ParameterFiles/PceParamInstance.json"
    
    #Path of PCE executable
    el["PCE_ExePath"]=SelfPath+"/MatlabScripts"
    #Name of the PCE executable
    el["PCE_ExeName"]="pceExe"
    #PCE executable
    el["PCE_Exe"]=el["PCE_ExePath"]+"/"+el["PCE_ExeName"]
    #Settings file for PCE execution model
    el["PCE_ModelSetRunFile"]=el["PCE_ExePath"]+"/PCE_Settings.json"
    #Elastix executable 
    el["elastixExe"]="/scratch/ggunay/Tools/elastix/src/bin/elastix"
    #Transformix executable
    el["transformixExe"]="/scratch/ggunay/Tools/elastix/src/bin/transformix"
    el["Pce_WeightFile"]=el["registRootDir"]+"/PceWeights.txt"
    
def runSimulated():
    mc=MC()
    setupEnvSimulatedData(mc)
    
    W=100
    mc.isVerbose(True)
    mc["RegMainDir"]=mc["registRootDir"]
    
    """"[ParamName,ParamDist,Param,ParamMean,ParamStd]"""
    """For uniform distribution ParamMean is the lower, ParamStd is the higher dist. boundary"""

    Data = Dataset()
    
    clusterProcessNumberUppperLimit=50
    
    mc.elastixSetClusterCommand("bigrsub -R 1.5G -q day ")
    mc.transformixSetClusterCommand("bigrsub -R 1.5G -q day ")
    mc.setWaitClusterFunc(waitCluster)
    for it in Data:
        mc["fixedIm"] = it["fixedIm"]
        mc["movingIm"] = it["movingIm"]
        mc.setParams(it["parameters"])
        mc.run(W, clusterProcessNumberUppperLimit,False,True,False)
runSimulated()
