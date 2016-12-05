#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# createfileInformation.py argument



import os
import string
import sys
from PricePrediction import PricePrediction

def calulateMean(filename):
    mean = 0.0
    lines = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            l, name = line.strip().split(',')
            lines.append((l, name))

    count = 0
    del lines[0]
    for line in lines:
        if line[1] != "nan":
            count = count + 1
            mean = mean + float(line[1])
    if count != 0:
        mean = mean / count
    else:
        mean = 0
    return mean


def applyPredictionModels(filename):
    predictionObj = PricePrediction()
    randomWalkErr, arimaErr, mlpErr, rnnErr = predictionObj.applyPredictionModels(filename)
    return randomWalkErr, arimaErr, mlpErr, rnnErr


# START
if len(sys.argv) < 2:
    print "You need to have the group name in the parameter"
    exit(0)

# Get the groupname form the parameters
output_file = open(sys.argv[1] + ".info", "w");
output_file.write("Product,Mean,randomWalkErr,arimaErr,mlpErr,rnnErr\n")

#pass second arg as the path of data files.
path = sys.argv[2]
for file in os.listdir(path):
    filename = file
    file = path + "/" + file
    if os.path.isfile(file):
        if file.endswith(".full"):
            index = string.find(filename, ".")
            #Get product id from filename
            productId = filename[0:index]
            output_file.write(productId)
            output_file.write(",")
            output_file.write(repr(calulateMean(file)))

            # Apply prediction models and write the errors to file
            randomWalkErr, arimaErr, mlpErr, rnnErr = applyPredictionModels(file)
            output_file.write(",")
            output_file.write(str(randomWalkErr))
            output_file.write(",")
            output_file.write(str(arimaErr))
            output_file.write(",")
            output_file.write(str(mlpErr))
            output_file.write(",")
            output_file.write(str(rnnErr))

            output_file.write("\n")
            continue
        else:
            continue
