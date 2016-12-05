#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# createfileInformation.py argument



import os
import string
import sys
from fill_missing_values import FillMissingValues


#pass second arg as the path of data files.
path = sys.argv[1]
for file in os.listdir(path):
    filename = file
    file = path + "/" + file
    if os.path.isfile(file):
        if file.endswith(".csv"):
            print filename
            fmv = FillMissingValues()
            fmv.insert_missing_values(file)
            continue
        else:
            continue
    break
