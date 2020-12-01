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


from Parameter.Parameter import Parameter as Par
from ExpSettings.DatasetBase import DatasetBase
from ExpSettings.Dataset.TestMethod.Environment  import Environment

import os
import numpy as np

__selfPath = os.path.dirname(os.path.realpath(__file__))

#There are 5 coefficient arrays.
DATASET_SIZE = 5 

def GetDataset(ind):
    assert ind >= 0 or ind < DATASET_SIZE, "There are only {0:d} number of datasets.".format(DATASET_SIZE)
    coefficientLetter = ""
    if ind == 0:
        coefficientLetter = "a"
    if ind == 1:
        coefficientLetter = "b"
    if ind == 2:
        coefficientLetter = "c"
    if ind == 3:
        coefficientLetter = "d"
    if ind == 4:
        coefficientLetter = "e"
    return np.load("{0:s}/Coefficients/coefficient_{1:s}.npy".format(__selfPath, coefficientLetter))

def GetParameters():
    """Method Test"""
    par = []
    par1 = Par("x", "gauss", 4.12, 2.65)
    par2 = Par("y", "gauss", 4.37, 0.55)

    par.append(par1)
    par.append(par2)
    return par

class Dataset(DatasetBase):
    def __init__(self):
        pass

    def GetDatasetSize(self):
        return DATASET_SIZE

    def GetDatasetWithIndex(self, ind:int):
        return []
    
    def GetMethodExtensionParams(self, ind:int):
        return {"coefficients": [GetDataset(ind_) for ind_ in range(DATASET_SIZE)], "testFunction":"TestFunction1"}
    
    def GetModeExtensionParams(self, ind:int):
        return {"sampleSize": 20000, "batchSize":3, "isVector": False}
    
    def GetParameters(self, datasetIndex):
        return GetParameters()
    
    def GetEnvironment(self, rootDir):
        return Environment(rootDir)


