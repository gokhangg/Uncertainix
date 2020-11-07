# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:19:07 2020

@author: ghngu
"""
from RealImages.Dataset import Dataset as RealDataset
from SynteticImages.Dataset import Dataset as SynDataset
import Dataset.DatasetBase as Base



def CreateDataset(datasetType) -> Base:
    if datasetType == "Real":
        return RealDataset()
    if datasetType == "Synthetic":
        return SynDataset()
 