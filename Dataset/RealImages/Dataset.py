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

import os
from ParameterSettings.Parameter import Parameter as Par
from Dataset.DatasetBase import DatasetBase

__selfPath = os.path.dirname(os.path.realpath(__file__))

__datasetRoot = "/hdd2/DataSet/FromLuu/DataSetJournalPaper"
__pointsetDir = ""

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

def getFixedImDtPath(__dict, __key):
    return __datasetRoot + "/SegmentationsFixed/" + getPatientExtension(__dict, __key) + "/Pre_dtout.mhd"

def getFullDatasetInfo(__dict, __key):
    retVal = {"key":__key, "val":__dict[__key]}
    retVal.update({"fixedIm": getFixedImPath(__dict, __key)})
    retVal.update({"movingIm": getMovingImPath(__dict, __key)})
    retVal.update({"fixedSeg": getFixedImSegPath(__dict, __key)})
    retVal.update({"movingSeg": getMovingImSegPath(__dict, __key)})
    retVal.update({"fixedSegDt": getFixedImDtPath(__dict, __key)})
    retVal.update({"pointSet":__selfPath + "/PointSets_MI/" + getPatientExtension(__dict, __key) + getIntraExtension(__dict, __key) + ".txt"})
    return retVal

def getAllDatasets():
    return [getFullDatasetInfo(__datasets, __key) for __key in __datasets]

def GetParameters():
    """Real Dataset"""
    par = []
    """Real Dataset"""
    par1 = Par("Metric1Weight", "gauss", 3.3, 2.8)
    """Real Dataset"""
    par2 = Par("Metric2Weight", "gauss", -8.0, 1.2)
    """Real Dataset"""
    par3 = Par("FinalGridSpacingInPhysicalUnits", "gauss", 6.0, 0.5)

    par.append(par1)
    par.append(par2)
    par.append(par3)
    return par

def GetRegistrationParamFiles():
    retVal = {}
    retVal.update({"RigidParamFile": __selfPath + "/ParameterFilesPCEstochastic/Rigidpara.txt"})
    retVal.update({"NonRigidParamFile": __selfPath + "/ParameterFilesPCEstochastic/Nonrigidpara.txt"})
    return retVal

def GetElastixParameters():
    paramDict = {"MethodParameters": GetParameters()}
    paramDict.update({"MethodParameterExtension": {"ELastixParameterFiles": GetRegistrationParamFiles()} })
    return paramDict
    
    

class Dataset(DatasetBase):
    def __init__(self):
        self.__dataset = getAllDatasets()
        self.__methodParameters = GetElastixParameters()        

    def GetDatasetSize(self):
        return len(self.__dataset)
    
    def GetDatasetWithIndex(self, ind):
        return self.__dataset[ind]
    
    def GetMethodParameters(self, ind):
        paramDict = self.__methodParameters
        extensionDict = {"-dt": self.__dataset[ind]["fixedSegDt"]}
        extensionDict.update({"-fp": self.__dataset[ind]["pointSet"]})
        
        paramDict.update({"MethodParameterExtension": {"CommandlineParameters": GetRegistrationParamFiles()} })
        return paramDict




