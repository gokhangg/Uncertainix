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
from ItkHandler.ItkHandler import  ItkHandler
import Method.TestMethod.TestFunctions as TestFunctions
from Method.MethodB import MethodB as Base

def GetValuesFromParamList(ls_, ind_):
    return [ls_[ind][ind_] for ind in range(len(ls_))]

class Method(Base):
    
    def __init__(self):
        self.__TestFunct = lambda a, b:0 * a[0]
    
    def SetMethodSettings(self, settings):
        self.__envDict = settings["environment"].GetEnvironmentDictForDataset(0,0)
        self.__parameters = settings["parameters"]
        self.__coefficients = settings["extension"]["coefficients"]
        if "testFunction" in settings["extension"]:
            self.__TestFunct = getattr(TestFunctions, settings["extension"]["testFunction"])
        

    def Run(self, in_):
        pass

    def IsFinished(self):
        return True   


    def GetResultsReady(self, indices: list):
        pass

    def GetResultWithIndex(self, ind_: int):
        par_ = GetValuesFromParamList(self.__parameters, ind_)
        imVol = self.__TestFunct(self.__coefficients, par_)
        itkIm = ItkHandler()
        itkIm.SetImageOrigin([0 for i_ in range(len(imVol.shape))])
        itkIm.SetImageSpacing([1 for i_ in range(len(imVol.shape))])
        itkIm.SetImageVolume(imVol)
        return itkIm
