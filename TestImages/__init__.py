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

import os

selfPath=os.path.dirname(os.path.realpath(__file__))


"""
@brief: Used to generate weights file from PCE executable for registration sampling locations .
@return: NA.
"""   
def getFixedImages():
    fixedImagesDict={"Image0":{"name":"ImFlatN"}}
    for ind in fixedImagesDict:
        fixedImagesDict[ind].update({"file":selfPath+"/"+fixedImagesDict[ind]["name"]+".mhd"})
    return fixedImagesDict

def getFixedImageSegmentations():
    fixedImageSegmentationsDict={"Image0":{"name":"ImFlat"}}
    for ind in fixedImageSegmentationsDict:
        fixedImageSegmentationsDict[ind].update({"file":selfPath+"/"+fixedImageSegmentationsDict[ind]["name"]+".mhd"})
    return fixedImageSegmentationsDict

def getMovingImages():
    movingImagesDict={}
    for ind in range(0,30):
        movingImagesDict.update({"Image"+str(ind):{"name":"Im"+str(ind)+"N","file":selfPath+"/Im"+str(ind)+"N.mhd"}})
    return movingImagesDict

def getMovingImageSegmentations():     
    movingImageSegmentationsDict={} 
    for ind in range(0,30):
        movingImageSegmentationsDict.update({"Image"+str(ind):{"name":"Im"+str(ind),"file":selfPath+"/Im"+str(ind)+".mhd"}})
    return movingImageSegmentationsDict