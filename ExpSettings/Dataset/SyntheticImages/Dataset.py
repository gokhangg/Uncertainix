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
from Parameter.Parameter import Parameter as Par
from ExpSettings.DatasetBase import DatasetBase

__selfPath = os.path.dirname(os.path.realpath(__file__))


def GetParameters():
    """Simulated Dataset"""
    par = []
    """Simulated Dataset"""
    par1 = Par("Metric1Weight", "gauss", 4.12, 2.65)

    """Simulated Dataset"""
    par2 = Par("FinalGridSpacingInPhysicalUnits", "gauss", 4.37, 0.55)

    par.append(par1)
    par.append(par2)
    return par

"""
@brief:  Used to generate weights file from PCE executable for registration sampling locations .
@return:  NA.
"""   

__DATASET_SIZE = 30

def GetFixedImage(ind: int):
    return __selfPath + "/Images/ImFlatN.mhd"

def GetFixedImageSegmentation(ind: int):
    return __selfPath + "/Images/ImFlat.mhd"

def GetMovingImage(ind: int):
    return __selfPath + "/Images/Im" + str(ind) + "N.mhd"

def GetMovingImageSegmentation(ind: int):
    return __selfPath + "/Images/Im" + str(ind) + ".mhd"

def GetRegistrationParamFiles():
    retVal = {}
    retVal.update({"RigidParamFile": __selfPath + "/RegistrationParameterFiles/RigidparaPI.txt"})
    retVal.update({"NonRigidParamFile": __selfPath + "/RegistrationParameterFiles/NonrigidparaPI.txt"})
    return retVal

def GetDataset(ind: int):
    retVal = {}
    retVal.update({"fixedIm": GetFixedImage(ind)})
    retVal.update({"movingIm": GetMovingImage(ind)})
    retVal.update({"fixedSeg": GetFixedImageSegmentation(ind)})
    retVal.update({"movingSeg": GetMovingImageSegmentation(ind)})
    return retVal

def GetPceSettingsFile():
    return __selfPath + "/PceSettings.json"


class Dataset(DatasetBase):
    def __init__(self):
        pass

    def GetDatasetSize(self):
        return __DATASET_SIZE

    def GetDatasetWithIndex(self, ind:int):
        return GetDataset(ind)
    
    def GetMethodExtensionParams(self, ind:int):
        return {"CommandlineParameters": None, "ParameterFiles": GetRegistrationParamFiles()}
    
    def GetModeExtensionParams(self, ind:int):
        return {"PceSettingsFile": GetPceSettingsFile()}
    
    def GetParameters(self, datasetIndex):
        return GetParameters()


