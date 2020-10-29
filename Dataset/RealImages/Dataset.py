# *=========================================================================
# *
# *  Copyright Erasmus MC Rotterdam and contributors
# *  This software is licensed under the Apache 2 license, quoted below.

# *  Copyright 2019 Erasmus MC Rotterdam.
# *  Copyright 2019 Gokhan Gunay <g.gunay@erasmsumc.nl>

# *  Licensed under the Apache License, Version 2.0 (the "License"); you may not
# *  use this file except in compliance with the License. You may obtain a copy of
# *  the License at
# *  http: //www.apache.org/licenses/LICENSE-2.0

# *  Unless required by applicable law or agreed to in writing, software
# *  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# *  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# *  License for the specific language governing permissions and limitations under
# *  the License.
# *=========================================================================

import os, sys
import Misc.Param as Par

__selfPath = os.path.dirname(os.path.realpath(__file__))

__datasetRoot = "/hdd2/DataSet/FromLuu/DataSetJournalPaper"

"""Training Dataset"""
__datasets = {"Dataset0":{"Patient":"Patient1", "Intra":"Intra01"}}
__datasets.update({"Dataset1":{"Patient":"Patient1", "Intra":"Intra02"}})
__datasets.update({"Dataset2":{"Patient":"Patient2", "Intra":"Intra01"}})
__datasets.update({"Dataset3":{"Patient":"Patient3", "Intra":"Intra02_rot"}})
__datasets.update({"Dataset4":{"Patient":"Patient5", "Intra":"Intra01"}})
__datasets.update({"Dataset5":{"Patient":"Patient5", "Intra":"Intra02"}})
__datasets.update({"Dataset6":{"Patient":"Patient8", "Intra":"Intra7"}})
__datasets.update({"Dataset7":{"Patient":"Patient27", "Intra":"Intra01"}})
__datasets.update({"Dataset8":{"Patient":"Patient28", "Intra":"Intra02"}})


"""Test Dataset"""
__datasets.update({"Dataset9":{"Patient":"Patient1", "Intra":"Intra03"}})
__datasets.update({"Dataset10":{"Patient":"Patient6", "Intra":"Intra13"}})
__datasets.update({"Dataset11":{"Patient":"Patient7", "Intra":"Intra01"}})
__datasets.update({"Dataset12":{"Patient":"Patient9", "Intra":"Intra02"}})


#__datasets.update({"Dataset9":{"Patient":"Patient12", "Intra":"Intra04"}})
#__datasets.update({"Dataset10":{"Patient":"Patient13", "Intra":"Intra05"}})
#__datasets.update({"Dataset11":{"Patient":"Patient13", "Intra":"Intra06"}})
#__datasets.update({"Dataset12":{"Patient":"Patient15", "Intra":"Intra07"}})
#__datasets.update({"Dataset13":{"Patient":"Patient14", "Intra":"Intra03"}})
#__datasets.update({"Dataset14":{"Patient":"Patient16", "Intra":"Intra04"}})
#__datasets.update({"Dataset15":{"Patient":"Patient18", "Intra":"Intra04"}})
#__datasets.update({"Dataset16":{"Patient":"Patient21", "Intra":"Intra01"}})
#__datasets.update({"Dataset17":{"Patient":"Patient23", "Intra":"Intra01"}})






class zipIterator:
    def __init__(self, val):
        self.__val = val

    def __iter__(self):
        return self

    def __next__(self):
        return self.__val

def getPatientExtension(__dict, __key):
    return __dict[__key]["Patient"]

def getIntraExtension(__dict, __key):
    return __dict[__key]["Intra"]

def getFixedImPath(__dict, __key):
    return __datasetRoot + "/Intra/" + getPatientExtension(__dict, __key) + "/" + getIntraExtension(__dict, __key) + ".mhd"

def getFixedImSegPath(__dict, __key):
    return __datasetRoot + "/SegmentationsFixed/" + getPatientExtension(__dict, __key) + "/" + getIntraExtension(__dict, __key) + ".mhd"

def getMovingImPath(__dict, __key):
    return __datasetRoot + "/PreandPost/" + getPatientExtension(__dict, __key) + "/Pre.mhd"

def getMovingImSegPath(__dict, __key):
    return __datasetRoot + "/SegmentationsFixed/" + getPatientExtension(__dict, __key) + "/Pre.mhd"

def getFullDatasetInfo(__dict, __key):
    return {"key":__key, "val":__dict[__key], "fixedIm": getFixedImPath(__dict, __key), "movingIm": getMovingImPath(__dict, __key),
            "fixedSeg": getFixedImSegPath(__dict, __key), "movingSeg": getMovingImSegPath(__dict, __key)}

def getAllDatasets():
    alla = [getFullDatasetInfo(__datasets, __key) for __key in __datasets]
    return alla

def getParameters(args = {}):
    """Real Dataset"""
    par = []
    """Real Dataset"""
    par1 = Par("Metric1Weight", "gauss", 3.3, 2.8)
    """Real Dataset"""
    par2 = Par("Metric2Weight", "gauss", -8.0, 1.2)
    par2["registrationParams"] = {"-dt": __datasetRoot + "/SegmentationsFixed/" + str(args["val"]["Patient"]) + "/Pre_dtout.mhd",
                                  "-fp": __selfPath + "/PointSets_MI/" + str(args["val"]["Patient"]) + str(args["val"]["Intra"]) + ".txt"}
    """Real Dataset"""
    par3 = Par("FinalGridSpacingInPhysicalUnits", "gauss", 6.0, 0.5)

    par1.setValMapFunct(lambda a: pow(2, a))
    par2.setValMapFunct(lambda a: pow(2, a))
    par3.setValMapFunct(lambda a: pow(2, a))
    par.append(par1)
    par.append(par2)
    par.append(par3)
    return par

def getRegistrationParameters():
    retVal = {}
    retVal.update({"RigidParamFile": __selfPath + "/ParameterFilesPCEstochastic/Rigidpara.txt"})
    retVal.update({"NonRigidParamFile": __selfPath + "/ParameterFilesPCEstochastic/Nonrigidpara.txt"})
    return retVal

class Dataset(object):
    def __init__(self):
        self.__dictionary = {}
        self.__iterationCount = 0
        self.bindDataSetsToParams()

    def getDatasetNumber(self):
        return len(self.__fixedImages)

    def getDatasetWithIndex(self, ind):
        return self["Dataset"+str(ind)]

    def resetIterator(self):
        self.__iterationCount = 0

    def getRegistrationParameters(self):
        return getRegistrationParameters()

    def __getitem__(self, key):
      	try:
            return self.__dictionary[key]
      	except:
            return ""

    def __setitem__(self, key, value):
        return self.__dictionary.update({key: value})

    def __iter__(self):
        return 5#self

    def __next__(self):
        if self.__iterationCount == len(self.__dictionary):
            return StopIteration
        else:
            self.__iterationCount += 1
            return 5#self["DataSet"+str(self.__iterationCount-1)]


    """
    @brief:  Some parameters to be analyze require extra information for the registration process.
            Such as "point to surface penalty" requries moving image distance transform or segmentation and fixed image point
            set. This function is used to add up those information to the parameters.
    @return:  NA.
    """
    def bindDataSetsToParams(self):
        for ind, it in enumerate(getAllDatasets()):
            
            it.update({"parameters": getParameters(it)})
            self[it["key"]] = it.copy()


