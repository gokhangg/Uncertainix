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
import PceHandler.PceHandler as PCE
import Misc.MatlabExeCompiler as MatlabCompiler
from DatasetsAndParameters import Dataset

if sys.version_info[0]==3:
    import subprocess
    exeGetOutput=subprocess.getoutput
else:
    import commands
    exeGetOutput=commands.getoutput
    
SelfPath=os.path.dirname(os.path.realpath(__file__))

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


"""
@brief: This method is a template to show which and how settings dictionaries
        should be assigned.
"""
def setupEnvSimulatedDataOld(inputDict):
     #Root Dir where the results to be saved
    inputDict["RootDir"]="/scratch/ggunay/TrialReal/SimulationDataTest"
    inputDict["resultsRootDir"]=inputDict["RootDir"]+"/ExpResults/PCE"
    #Rootdir where registration results to be saved
    inputDict["registRootDir"]=inputDict["resultsRootDir"]
    #Path of Intra dataset
    inputDict["fixedDatasetPath"]=inputDict["RootDir"]+"/TestImages"
    #Path of Pre dataset
    inputDict["movingDatasetPath"]=inputDict["RootDir"]+"/TestImages"
    #Path of segmentation dataset
    inputDict["segDatasetPath"]=inputDict["RootDir"]+"/TestImages"

    #Rigid registration parameter file template
    inputDict["rigidParaTemplate"]=inputDict["RootDir"]+"/ParameterFiles/RigidparaPI.txt"
    #Nonrigid registration parameter file template
    inputDict["nonRigidParaTemplate"]=inputDict["RootDir"]+"/ParameterFiles/Nonrigidpara2ndStep.txt"
    #Example settings for PCE execution model
    inputDict["PceSetInstanceFile"]=inputDict["RootDir"]+"/ParameterFiles/PceParamInstance.json"
    
    #Path of PCE executable
    inputDict["PCE_ExePath"]=SelfPath+"/MatlabScripts"
    #Name of the PCE executable
    inputDict["PCE_ExeName"]="pceExe"
    #PCE executable
    inputDict["PCE_Exe"]=inputDict["PCE_ExePath"]+"/"+inputDict["PCE_ExeName"]
    #Settings file for PCE execution model
    inputDict["PCE_ModelSetRunFile"]=inputDict["PCE_ExePath"]+"/PCE_Settings.json"
    #Elastix executable 
    inputDict["elastixExe"]="/scratch/ggunay/Tools/elastix/src/bin/elastix"
    #Transformix executable
    inputDict["transformixExe"]="/scratch/ggunay/Tools/elastix/src/bin/transformix"
    inputDict["Pce_WeightFile"]=inputDict["registRootDir"]+"/PceWeights.txt"

def setupEnvRealDataOld(el):
     #Root Dir where the results to be saved
    el["RootDir"]="/scratch/ggunay/TrialReal/RealData2"
    el["resultsRootDir"]=el["RootDir"]+"/ExpResults/PCE"
    #Rootdir where registration results to be saved
    el["registRootDir"]=el["resultsRootDir"]
    #Path of Intra dataset
    el["fixedDatasetPath"]="/archive/ggunay/DataSetJournalPaper/Intra/Patient2"
    #Path of Pre dataset
    el["movingDatasetPath"]="/archive/ggunay/DataSetJournalPaper/PreandPost/Patient2"
    #Path of segmentation dataset
    el["segDatasetPath"]="/archive/ggunay/DataSetJournalPaper/SegmentationsFixed/Patient2"

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
    
    el["fixedIm"]=el["fixedDatasetPath"]+"/Intra01.mhd"
    el["movingSegmentationDT"]=el["segDatasetPath"]+"/Pre_dtout.mhd"
    el["movingIm"]=el["movingDatasetPath"]+"/Pre.mhd"

def setupEnvSimulatedData(el):
     #Root Dir where the results to be saved
    el["RootDir"]=SelfPath
    el["resultsRootDir"]=el["RootDir"]+"/ExpResults/PCE"
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
    
    compiler=MatlabCompiler()
    compiler["preCommands"]="module load matlab & module load mcr &"
    compiler["postCommands"]=""
    compiler.compileMatlabExe()
    
    pce=PCE()
    pce["prePceCommands"]="module load matlab & module load mcr &"
    pce["postPceCommands"]=""
    setupEnvSimulatedData(pce)
    pce.isVerbose(True)
    
    """"[ParamName,ParamDist,Param,ParamMean,ParamStd]"""
    """For uniform distribution ParamMean is the lower, ParamStd is the higher dist. boundary"""
        
    pce.setQuadratureType("gauss")
    pce.setGridType("sparse")
    pce.setTrim("1")
    pce.setRemoveSmallElements("1")
    pce.setSmallElementThresh("1e-13")    
    
    pce.elastixSetClusterCommand("bigrsub -R 1.5G -q day ")
    pce.setClusterWaitFunc(waitCluster)
    
    """
    Format: {"Image Name in the dataset table":{"name":Real image name,"file":Image file name with full path}}
        Image file name =Images["Image Name in the dataset table"]["file"]
    """

    Data = Dataset()
    """
    Here we assert which uncertainies will be produced using Sobol decomposition.
    """
    pce["uncertaintyGroup"] = "1-2-1_2-all"
    for ind in range(0, Data.getDatasetNumber()):
        it = Data.getDatasetWithIndex(ind)
        for ind2 in [3]:
            for ind3 in [3]:
                pce.setPolOrder(ind2)
                pce.setGridLevel(ind3)
                
                pce["fixedIm"] = it["fixedIm"]
                pce["movingIm"] = it["movingIm"]
                pce.setParams(it["parameters"])
                
                pce["RegMainDir"]=pce["registRootDir"]+"/Dataset"+str(ind)+"/""Gl"+str(ind2)+"Po"+str(ind3)
                pce.run(False, True)

runSimulated()