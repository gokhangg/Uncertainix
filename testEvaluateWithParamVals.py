import numpy as np
import sys,os,time
import SimpleITK as sitk

if sys.version_info[0]==3:
    import subprocess
    exeGetOutput=subprocess.getoutput
else:
    import commands
    exeGetOutput=commands.getoutput

sys.path.append("./Uncertainix")
sys.path.append("./Uncertainix/lib")
sys.path.append("./Uncertainix/TestImages")
selfPath=os.path.dirname(os.path.realpath(__file__))

import lib
import TestImages as Images

"""
@brief: Reads an image.
@param: fileName Name of the file to be read.
@return: ItkImage contains image array and spatial coordinate details.
"""
def loadItkImage(filename):
    itkimage = sitk.ReadImage(filename)
    vol = sitk.GetArrayFromImage(itkimage)
    origin = np.array(list(reversed(itkimage.GetOrigin())))
    spacing = np.array(list(reversed(itkimage.GetSpacing())))
    return vol, origin, spacing 

def getgetSamplePointsRange(mean,std,stepSize):
    start=mean-2*std
    stop=mean+2*std
    return [start,stop,(stop-start)/stepSize]

def getMeshPoints(rangeList):
    x = np.arange(rangeList[0][0], rangeList[0][1], rangeList[0][2])
    y = np.arange(rangeList[1][0], rangeList[1][1], rangeList[1][2])
    return [np.meshgrid(x, y)[0].reshape(-1), np.meshgrid(x, y)[1].reshape(-1)]

def getValueFromCoordinates(meshGrid, x, y):
    return [meshGrid[1][x, y], meshGrid[0][x, y]]


def waitCluster():
    Qstat = exeGetOutput("qstat ")
    cnt = 0
    while Qstat.count("\n") > 1:
        Qstat = exeGetOutput("qstat ")
        if not cnt == Qstat.count("\n"):
            cnt = Qstat.count("\n")
            print("Remaining Task ", cnt - 1)
        time.sleep(2)

def writeSampleMesh(fileName,sampleMesh):
    fl = open(fileName, "w")
    for ind in range(0, len(sampleMesh[0])):
        fl.write(str(sampleMesh[0][ind]) + " " + str(sampleMesh[1][ind]) + "\n")
    fl.close()

""""number of samples in each direction"""
sampNum=10

def setupEnvSimulatedData(el):
    # Root Dir where the results to be saved
    el["RootDir"] = selfPath
    el["resultsRootDir"] = el["RootDir"] + "/ExpResults/MC"
    # Rootdir where registration results to be saved
    el["registRootDir"] = el["resultsRootDir"]
    # Rigid registration parameter file template
    el["rigidParaTemplate"] = el["RootDir"] + "/ParameterFiles/RigidparaPI.txt"
    # Nonrigid registration parameter file template
    el["nonRigidParaTemplate"] = el["RootDir"] + "/ParameterFiles/Nonrigidpara2ndStep.txt"
    # Elastix executable
    el["elastixExe"] = "/scratch/ggunay/Tools/elastix/src/bin/elastix"
    # Transformix executable
    el["transformixExe"] = "/scratch/ggunay/Tools/elastix/src/bin/transformix"
    el["Pce_WeightFile"] = el["registRootDir"] + "/PceWeights.txt"


def setupEnvSimulatedDataPCE(el):
    # Root Dir where the results to be saved
    el["RootDir"] = selfPath
    el["resultsRootDir"] = el["RootDir"] + "/ExpResults/PCE"
    # Rootdir where registration results to be saved
    el["registRootDir"] = el["resultsRootDir"]

    # Rigid registration parameter file template
    el["rigidParaTemplate"] = el["RootDir"] + "/ParameterFiles/RigidparaPI.txt"
    # Nonrigid registration parameter file template
    el["nonRigidParaTemplate"] = el["RootDir"] + "/ParameterFiles/Nonrigidpara2ndStep.txt"
    # Example settings for PCE execution model
    el["PceSetInstanceFile"] = el["RootDir"] + "/ParameterFiles/PceParamInstance.json"

    # Path of PCE executable
    el["PCE_ExePath"] = el["RootDir"] + "/MatlabScripts"
    # Name of the PCE executable
    el["PCE_ExeName"] = "pceExe"
    # PCE executable
    el["PCE_Exe"] = el["PCE_ExePath"] + "/" + el["PCE_ExeName"]
    # Settings file for PCE execution model
    el["PCE_ModelSetRunFile"] = el["PCE_ExePath"] + "/PCE_Settings.json"
    # Elastix executable
    el["elastixExe"] = "/scratch/ggunay/Tools/elastix/src/bin/elastix"
    # Transformix executable
    el["transformixExe"] = "/scratch/ggunay/Tools/elastix/src/bin/transformix"
    el["Pce_WeightFile"] = el["registRootDir"] + "/PceWeights.txt"

def runExperiment():
    mc = lib.MonteCarlo()
    setupEnvSimulatedData(mc)
    mc["RegMainDir"] = mc["registRootDir"]

    """Simulated Dataset"""
    par1 = lib.Param("Metric1Weight", "gauss", 4.12, 2.65)
    """Simulated Dataset"""
    par2 = lib.Param("FinalGridSpacingInPhysicalUnits", "gauss", 4.37, 0.55)

    rangePar1 = getgetSamplePointsRange(par1.getMean(), par1.getStd(), sampNum)
    rangePar2 = getgetSamplePointsRange(par2.getMean(), par2.getStd(), sampNum)
    sampleMesh = getMeshPoints([rangePar1, rangePar2])
    
    if not os.path.isdir(mc["resultsRootDir"]):
        os.makedirs(mc["resultsRootDir"], mode=0o777)
    mc["sampleMeshFile"] = mc["resultsRootDir"]+"/sampleMesh.txt"
    writeSampleMesh(mc["sampleMeshFile"], sampleMesh)
    
    par1.setVals(sampleMesh[0])
    par2.setVals(sampleMesh[1])

    par1.setValMapFunct(lambda a: pow(2, a))
    par2.setValMapFunct(lambda a: pow(2, a))
    par1.mapVal()
    par2.mapVal()
    mc.addParam(par1)
    mc.addParam(par2)
    mc.setSampleNum(par1.getSize())

    mc.elastixSetClusterCommand("bigrsub -R 1.5G -q day ")
    mc.transformixSetClusterCommand("bigrsub -R 1.5G -q day ")
    mc.setWaitClusterFunc(waitCluster)

    fixedImages = Images.getFixedImages()
    movingImages = Images.getMovingImages()

    mc["fixedIm"] = fixedImages["Image0"]["file"]
    mc["movingIm"] = movingImages["Image0"]["file"]

    mc.elastixOnCluster(False)
    mc.runRig()
    mc.waitCluster()
    mc.elastixOnCluster(True)
    print("num: ", mc.getSampleNum())
    for cnt in range(0, mc.getSampleNum()):
        mc.runNonRigSingle(cnt)
    mc.waitCluster()
    

    mc.transformixOnCluster(True)
    for index in range(0, mc.getSampleNum()):
        mc["defFieldDir"] = mc["RegMainDir"] + "/NonRigid/Trans" + str(index)
        mc["nonRigRegDir"] = mc["RegMainDir"] + "/NonRigid/Elas" + str(index)
        mc.getDeformationField()
    mc.waitCluster()
    return sampleMesh, mc

def runExperimentPCE():
    compiler = lib.MatlabExeCompiler()
    compiler["preCommands"]="module load matlab & module load mcr &"
    compiler["postCommands"]=""
    compiler.compileMatlabExe()

    pce = lib.PceHandler()
    pce["prePceCommands"] = "module load matlab & module load mcr &"
    pce["postPceCommands"] = ""
    setupEnvSimulatedDataPCE(pce)
    pce.isVerbose(True)

    """Simulated Dataset"""
    par1 = lib.Param("Metric1Weight", "gauss", 4.12, 2.65)

    """Simulated Dataset"""
    par2 = lib.Param("FinalGridSpacingInPhysicalUnits", "gauss", 4.37, 0.55)

    rangePar1 = getgetSamplePointsRange(0, par1.getStd(), sampNum)
    rangePar2 = getgetSamplePointsRange(0, par2.getStd(), sampNum)
    sampleMesh = getMeshPoints([rangePar1, rangePar2])

    if not os.path.isdir(pce["resultsRootDir"]):
        os.makedirs(pce["resultsRootDir"], mode=0o777)

    pce["sampleMeshFile"] = pce["resultsRootDir"]+"/sampleMesh.txt"
    writeSampleMesh(pce["sampleMeshFile"], sampleMesh)

    par1.setValMapFunct(lambda a: pow(2, a))
    pce.addParam(par1)

    par2.setValMapFunct(lambda a: pow(2, a))
    pce.addParam(par2)

    pce.setQuadratureType("gauss")
    pce.setGridType("sparse")
    pce.setTrim("1")
    pce.setRemoveSmallElements("1")
    pce.setSmallElementThresh("1e-13")

    pce.elastixSetClusterCommand("bigrsub -R 1.5G -q day ")
    pce.setClusterWaitFunc(waitCluster)

    fixedImages = Images.getFixedImages()
    movingImages = Images.getMovingImages()

    polOrder = 3
    gridLevel = 3

    pce.setPolOrder(polOrder)
    pce.setGridLevel(gridLevel)

    pce["fixedIm"] = fixedImages["Image0"]["file"]
    pce["movingIm"] = movingImages["Image0"]["file"]

    pce["RegMainDir"] = pce["registRootDir"] + "/" + movingImages["Image0"]["name"] + "/""Gl" + str(gridLevel) + "Po" + str(polOrder)

    rigOnCluster = False
    pce.elastixOnCluster(rigOnCluster)
    pce.runRig()
    pce.generatePceParamFile()
    pce.generateWeightFile()
    pce.loadWeightFromFile()
    pce.clusterWait()
    nonRigOnCluster = True
    pce.elastixOnCluster(nonRigOnCluster)
    pce.runAllNonRigidReg()
    pce.clusterWait()

    pce["stdImageFile"] = pce["RegMainDir"] + "/stdImage.mhd"
    for cnt in range(0, par1.getSize()):
        pce["defFieldDir"] = pce["RegMainDir"] + "/NonRigid/Transformix" + str(cnt)
        pce["nonRigRegDir"] = pce["RegMainDir"] + "/NonRigid/Elastix" + str(cnt)
        pce.getDeformationField()
    pce.clusterWait()

    cmd = pce["prePceCommands"]
    cmd += pce["PCE_Exe"] + " -rootDir " + pce[
        "RegMainDir"] + " -verbose -Evaluate "+ pce["sampleMeshFile"] + " -outDir " + pce[
               "RegMainDir"] + " -settingsFile " + pce["PCE_ModelSetRunFile"] + " -runPCE "
    cmd += pce["postPceCommands"]
    os.system(cmd)

    return sampleMesh, pce

pixelLoc = [243, 233]
sampleMesh, mc =runExperiment()
_, pce = runExperimentPCE()

if 1:
    fl = open(pce["RootDir"]+"/ExpResults/diff.txt","w")
    for ind in range(1, len(sampleMesh[0])+1):
        file = pce["RegMainDir"]+"/Gl"+str(pce.getGridLevel())+"Po"+str(pce.getPolOrder())+"Scen"+str(ind)+".mhd"
        valPce = loadItkImage(file)[0].reshape(-1)
        file = mc["RegMainDir"] + "/NonRigid/Trans" + str(ind-1)+"/deformationField.mhd"
        valMc = loadItkImage(file)[0].reshape(-1)
        amp = np.abs(valMc).mean()
        meanDiff = np.abs(valMc-valPce).mean()
        fl.write(str(sampleMesh[0][ind-1])+" "+str(sampleMesh[1][ind-1])+" "+str(amp)+" "+str(meanDiff)+"\n")
    fl.close()
    for ind0 in range(0,16):
        for ind1 in range(0,16):
            fl = open(mc["RootDir"]+"/ExpResults/valueListMC"+str(32*ind0)+"_"+str(32*ind1)+".txt","w")
            for ind in range(0,len(sampleMesh[0])):
                file = mc["RegMainDir"] + "/NonRigid/Trans" + str(ind)+"/deformationField.mhd"
                val = loadItkImage(file)[0][32*ind0, 32*ind1]
                fl.write(str(sampleMesh[0][ind])+" "+str(sampleMesh[1][ind])+" "+str(val)+"\n")
            fl.close()
            
            fl = open(pce["RootDir"]+"/ExpResults/valueListPCE"+str(32*ind0)+"_"+str(32*ind1)+".txt","w")
            for ind in range(1, len(sampleMesh[0])+1):
                file = pce["RegMainDir"]+"/Gl"+str(pce.getGridLevel())+"Po"+str(pce.getPolOrder())+"Scen"+str(ind)+".mhd"
                val = loadItkImage(file)[0][32*ind0, 32*ind1]
                fl.write(str(sampleMesh[0][ind-1])+" "+str(sampleMesh[1][ind-1])+" "+str(val)+"\n")
            fl.close()