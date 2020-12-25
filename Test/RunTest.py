
import os, sys

selfPath = os.path.dirname(__file__)
parentPath = os.path.dirname(selfPath)
sys.path += [parentPath]

from Imp.Imp import Implementation
from ItkHandler.ItkHandler import  ItkHandler


import numpy as np
import unittest

TEST_EQUALITYRATIO_DELTA = 1e-1

def CreateTestResult(mode_):
    imp = Implementation("TestMethod", selfPath)
    imp.SelectMethod("TestMethod")
    imp.SelectMode(mode_)
    imp.Run(0)

    return imp.GetResult()


class TestPCE(unittest.TestCase):

    def test_stdMultiVarFunctions(self):
        pceRes = CreateTestResult("Pce")
        mcRes = CreateTestResult("MonteCarlo")
        pceResIm = ItkHandler()
        mcResIm = ItkHandler()
        pceResIm.LoadImage(pceRes)
        mcResIm.LoadImage(mcRes)
        imPce = pceResIm.GetImageVolume().reshape(-1)
        imMc = mcResIm.GetImageVolume().reshape(-1)
        diff = np.abs((imPce - imMc) / imMc)
        sz = diff.size
        diff = diff.sum() / sz
        self.assertAlmostEqual(diff, 0, delta = TEST_EQUALITYRATIO_DELTA)


if __name__ == '__main__':
    unittest.main()