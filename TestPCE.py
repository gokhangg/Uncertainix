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
import lib.PceHandler as PCE
import lib.Param as PR
import lib.MatlabExeCompiler as MatlabCompiler
import TestImages as Images

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
def setupEnvSimulatedData(inputDict):
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

def setupEnvRealData(el):
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

    """Simulated Dataset"""
    par1=PR("Metric1Weight","gauss",4.12,2.65)
    
    """Simulated Dataset"""
    par2=PR("FinalGridSpacingInPhysicalUnits","gauss",4.37,0.55)

    par1.setValMapFunct(lambda a:pow(2,a)) 
    pce.addParam(par1)
    
    par2.setValMapFunct(lambda a:pow(2,a))
    pce.addParam(par2)
        
    pce.setQuadratureType("gauss")
    pce.setGridType("sparse")
    pce.setTrim("1")
    pce.setRemoveSmallElements("1")
    pce.setSmallElementThresh("1e-13")    
    
    pce.elastixSetClusterCommand("bigrsub -R 1.5G -q day ")
    pce.setClusterWaitFunc(waitCluster)
    
    fixedImages=Images.getFixedImages()
    movingImages=Images.getMovingImages()
    
    for ind in movingImages:
        for ind2 in [3]:
            for ind3 in [3]:
                pce.setPolOrder(ind2)
                pce.setGridLevel(ind3)
                
                pce["fixedIm"]=fixedImages["Image0"]["file"]
                pce["movingIm"]=movingImages[ind]["file"]     
                
                pce["RegMainDir"]=pce["registRootDir"]+"/"+movingImages[ind]["name"]+"/""Gl"+str(ind2)+"Po"+str(ind3)
                pce.run(False,True)

runSimulated()