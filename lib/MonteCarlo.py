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

import numpy as np
import os, shutil
from ElastixHandler import *
from Param import *
from itk_handler import *

__selfPath = os.path.dirname(os.path.realpath(__file__))


class MonteCarlo(Elastix):
    __verbose = False

    def __init__(self):
        super(MonteCarlo, self).__init__()
        self.__sum = 0
        self.__pow2 = 0
        self.__meanArr = [0.0]
        self.__stdArr = [1.0]
        self.__sampleNum = 10
        self.__randVarTypeArr = ["gauss"]
        self.__paramsToAnalyze = []
        self.__selfParams = {}
        self.__waitClusterFunc = lambda param: param
        self.__loadFrompreviousRun = False
        self.__clusterBatchLim = 100
        self.__itk_handler = itk_handler()

    """
    @brief: Runs the experiment.
    @param: sampleNum Assigns number of samples in the experiment.
    @param: clusterBatchLim Sets upper limit of number of parallel processes on 
                on the cluster.
    @param: transformixOnCluster Sets if transformix runs on the cluster.
    @param: nonRigOnCluster Sets if non-rigid registration runs on the cluster.
    @param: rigOnCluster Sets if rigid registration runs on the cluster.
    @return: NA.
    @note: This method may be changed in accordance with user's desire.
    """

    def run(self, sampleNum=0, clusterBatchLim=50, transformixOnCluster=False, nonRigOnCluster=False,
            rigOnCluster=False):
        self.setSampleNum(sampleNum)
        self.generateParamVals()
        self.saveParams()
        self.elastixOnCluster(rigOnCluster)
        self.runRig()
        self.waitCluster()
        self.elastixOnCluster(nonRigOnCluster)
        for cnt in range(0,sampleNum):
            self.runNonRigSingle(cnt)
        self.waitCluster()
        self.transformixOnCluster(transformixOnCluster)
        self.setClusterBatchLim(clusterBatchLim)
        self.getStd()
        stdImage = self["RegMainDir"] + "/stdImage.mhd"
        self.saveStdImage(stdImage)

    """
    @brief: Saves estimated standard deviation image.
    @param: fileName File name to save the image.
    @return: NA.
    """

    def saveStdImage(self, fileName):
        try:
            self.__itk_handler.setFullImage(self.getStdImage())
            self.__itk_handler.saveImage(fileName, isVector=True)
        except:
            if self.__verbose:
                print("There occured a problem while saving standard deviation image.")

    """
    @brief: Returns calculated standard deviation image.
    @return: Standard deviation image.
    """

    def getStdImage(self):
        fullImage = [self.__stdImage, self.__ImageOrigin, self.__ImageSpacing]
        return fullImage

    """
    @brief: Calculates standard deviation vector-image from several 
            deformation fields.
    @return: NA.
    """

    def getStd(self):
        self.__estimateFirstAndSecondMoments()
        self.__stdImage = np.sqrt(np.abs(self.__pow2 - self.__sum ** 2))
        self.__sum = 0
        self.__pow2 = 0
        if self.__verbose:
            print("Standard deviation image is ready.")

    """
    @brief: Estimates first and second moments from dataset collection.
    @return: NA.
    """

    def __estimateFirstAndSecondMoments(self):
        div = int(self.__sampleNum / self.__clusterBatchLim)
        mod = int(self.__sampleNum % self.__clusterBatchLim)
        for index in range(0, div):
            startIndex = index * self.__clusterBatchLim
            endIndex = (index + 1) * self.__clusterBatchLim
            self.__getDeformationFields(startIndex, endIndex)
            self.waitCluster()
            self.__accumulateFirstAndSecondMoments(startIndex, endIndex)
        startIndex = div * self.__clusterBatchLim
        endIndex = mod + div * self.__clusterBatchLim
        self.__getDeformationFields(startIndex, endIndex)
        self.waitCluster()
        self.__accumulateFirstAndSecondMoments(startIndex, endIndex)
        self.__sum /= self.__sampleNum
        self.__pow2 /= self.__sampleNum

    """
    @brief: Adds up all partial first and second moments from dataset collection.
    @return: NA.
    """

    def __accumulateFirstAndSecondMoments(self, startIndex, endIndex):
        for index in range(startIndex, endIndex):
            self["defFieldDir"] = self["RegMainDir"] + "/NonRigid/Trans" + str(index)
            self.__itk_handler.loadImage(self["defFieldDir"] + "/deformationField.mhd")
            Vol = self.__itk_handler.getFullImage()
            self.__ImageOrigin = Vol[1]
            self.__ImageSpacing = Vol[2]
            try:
                self.__pow2 += Vol[0] * Vol[0]
                self.__sum += Vol[0]
            except:
                self.__ImageOrigin = Vol[1]
                self.__ImageSpacing = Vol[2]
            shutil.rmtree(self["defFieldDir"])

    """
    @brief: Used to get deformation field for a dataset.
    @return: NA.
    """

    def __getDeformationFields(self, startIndex, endIndex):
        for index in range(startIndex, endIndex):
            self["defFieldDir"] = self["RegMainDir"] + "/NonRigid/Trans" + str(index)
            self["nonRigRegDir"] = self["RegMainDir"] + "/NonRigid/Elas" + str(index)
            self.getDeformationField()

    """
    @brief: Runs rigid registration.
    @return: NA.
    """

    def runRig(self):
        self["rigRegDir"] = self["RegMainDir"] + "/Rigid"
        self.rigidElasRun()

    """
    @brief: Runs non-rigid registration with index.
    @return: NA.
    """

    def runNonRigSingle(self, ind):
        self["nonRigRegDir"] = self["RegMainDir"] + "/NonRigid/Elas" + str(ind)
        paramDict = {}
        elasParamDict = {}
        for it in self.__paramsToAnalyze:
            paramDict.update({it.getName(): it.getVals()[ind]})
            registrationParams = it["registrationParams"]
            for it2 in registrationParams:
                elasParamDict.update({it2: registrationParams[it2]})
        self.nonRigidElasRun(paramDict, elasParamDict)

    """
    @brief: Saves all parameters with their generated values.
    @param: path Path where the parameter files are to be saved.
    @return: NA
    """

    def saveParams(self, path=""):
        if path == "":
            path = self["resultsRootDir"] + "/ParamVals"
        if not os.path.isdir(path):
            os.makedirs(path)
        for ind, it in enumerate(self.__paramsToAnalyze):
            it.saveToFile(path + "/parameter" + str(ind) + ".txt")

    """
    @brief: Loads all saved parameters with their generated values.
    @param: path Path where the parameter files are to be sought.
    @return: Binary values signifying success of the attempt.
    """

    def loadParams(self, path=""):
        if path == "":
            path = self["registRootDir"] + "/ParamVals"
        if not os.path.isdir(path):
            if self.__verbose:
                print("there is no folder with the given name")
            return False
        for ind, it in enumerate(self.__paramsToAnalyze):
            if not os.path.isfile(path + "/parameter" + str(ind) + ".txt"):
                if self.__verbose:
                    print("there is no file with the given name")
                return False
        for ind, it in enumerate(self.__paramsToAnalyze):
            it.loadFromFile(path + "/parameter" + str(ind) + ".txt")
        return True

    """
    @brief: Generates or loads parameter values.
    @return: NA.
    """

    def generateParamVals(self):
        if self.__loadFrompreviousRun:
            if not self.loadParams():
                self.__getNewParamVal()
            return
        self.__getNewParamVal()

    """
    @brief: Generates values of
            the parameters according to given properties of parameters.
    @return: NA.
    """

    def __getNewParamVal(self):
        for cnt in range(0, len(self.__paramsToAnalyze)):
            self.__paramsToAnalyze[cnt].setSize(self.__sampleNum)
            self.__paramsToAnalyze[cnt].generateRandVal()
            self.__paramsToAnalyze[cnt].mapVal()

    """
    @brief: Selects verbose output.
    @param: verbose Binary value for verbose output.
    @return: NA
    """

    def isVerbose(self, verbose=False):
        self.__verbose = verbose
        super(MonteCarlo, self).isVerbose(verbose)

    """
    @brief: This method is used to assign a wait function to poll if the processes on the cluster are finished. 
            If there are still jobs to be finished the assigned wait function blocks proceeding to other processes.
    @param: waitFunction The waiting function (address) to be assigned.
    @return: NA
    """

    def setWaitClusterFunc(self, waitFunction):
        self.__waitClusterFunc = waitFunction

    """
    @brief: This method is called for waiting cluster.
    @return: NA
    """

    def waitCluster(self):
        self.__waitClusterFunc()

    """
    @brief: Sets number of samples in the procedure.
    @param: sampleNumber Sample number.
    @return: NA
    """

    def setSampleNum(self, sampleNumber=10):
        self.__sampleNum = sampleNumber

    """
    @brief: Gets number of samples in the procedure.
    @return: Sample number.
    """

    def getSampleNum(self):
        return self.__sampleNum

    """
    @brief: If parameters are required to be loaded from previous runs 
            this method activates loading.
    @param: fromPrevious Binary value signifying realization fo loading.
    @return: NA
    """

    def loadParamsFromPreviousRun(self, fromPrevious=False):
        self.__loadFrompreviousRun = fromPrevious

    """
    @brief: Adds a new parameter in the analysis.
    @param: param Parameter to be added.
    @return: NA
    """

    def addParam(self, param):
        self.__paramsToAnalyze += [param]

    """
    @brief: Returns all parameters in the analysis.
    @return: All parameters.
    """

    def getParams(self):
        return self.__paramsToAnalyze

    """
    @brief: Returns number of parameters in the analysis.
    @return: Number of parameters.
    """

    def getParamNum(self):
        return len(self.__paramsToAnalyze)

    """
    @brief: Sets upper limit to number of parallel processes on cluster.
    @param: lim Number limit.
    @return: NA.
    """

    def setClusterBatchLim(self, lim=100):
        self.__clusterBatchLim = lim

