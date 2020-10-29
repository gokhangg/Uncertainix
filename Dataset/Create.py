# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:19:07 2020

@author: ghngu
"""
from Realimages import Dataset as RealDataset
from Synteticimages import Dataset as SynDataset
from Dataset import DatasetBase as Base

    
def CreateReal() -> Base:
    return RealDataset()

def CreateSynthetic() -> Base:
    return SynDataset()
 