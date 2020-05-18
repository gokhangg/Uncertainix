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

selfPath=os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, "./Misc")
sys.path.insert(0, "../Misc")

class zipIterator:
    def __init__(self, val):
        self.__val = val

    def __iter__(self):
        return self

    def __next__(self):
        return self.__val

def getParameters():
    """Simulated Dataset"""
    par = []
    """Simulated Dataset"""
    par1 = Par("Metric1Weight", "gauss", 4.12, 2.65)

    """Simulated Dataset"""
    par2 = Par("FinalGridSpacingInPhysicalUnits", "gauss", 4.37, 0.55)

    par1.setValMapFunct(lambda a: pow(2, a))
    par2.setValMapFunct(lambda a: pow(2, a))
    par.append(par1)
    par.append(par2)
    return par

"""
@brief:  Used to generate weights file from PCE executable for registration sampling locations .
@return:  NA.
"""   
def getFixedImages():
    return [selfPath+"/ImFlatN.mhd" for ind in range(0,30)]

def getFixedImageSegmentations():
    return [selfPath+"/ImFlat.mhd" for ind in range(0,30)]

def getMovingImages():
    return [selfPath + "/Im"+str(ind)+"N.mhd" for ind in range(0, 30)]

def getMovingImageSegmentations():
    return [selfPath + "/Im"+str(ind)+".mhd" for ind in range(0, 30)]




class Dataset(object):
    def __init__(self):
        self.__parameters = getParameters()
        self.__fixedImages = getFixedImages()
        self.__movingImages = getMovingImages()
        self.__fixedImageSegmentations = getFixedImageSegmentations()
        self.__movingImageSegmentations = getMovingImageSegmentations()
        self.__dictionary = {}
        self.__iterationCount = 0
        if not len(self.__fixedImages) == len(self.__movingImages) == len(self.__fixedImageSegmentations) == len(self.__movingImageSegmentations):
            message = "Numbers of fixed, moving and their segmentations are not compatible."
            print(message)
            return message

        self.bindDataSetsToParams()


    def getDatasetNumber(self):
        return len(self.__fixedImages)

    def getDatasetWithIndex(self, ind):
        return self["DataSet"+str(ind)]

    def resetIterator(self):
        self.__iterationCount = 0

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
        for ind, [fixIm, movIm, fixSeg, movSeg] in enumerate(zip(self.__fixedImages, self.__movingImages, self.__fixedImageSegmentations, self.__movingImageSegmentations)):
            self["DataSet"+str(ind)] = {"fixedIm": fixIm, "movingIm": movIm, "fixedSeg": fixSeg, "movingSeg": movSeg, "parameters": self.__parameters}


