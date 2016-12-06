#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# createMeanErrorForCategory.py argument

import os
import string
import sys


# argument for this function is the error array
def calculateMeanForError(error):
    mean = 0.0
    count = 0
    for value in error:
        # print "value is :   " + value
        if not value[1]:
            continue
        if value == "None":
            continue
        elif value == "9999":
            continue
        else:
            count = count + 1
            mean = mean + float(value)
    if count != 0:
        mean = mean / count
    else:
        mean = 0
        # print "Error in calculating mean"
    return mean


def column(matrix, i):
    return [row[i] for row in matrix]


# START
if len(sys.argv) < 2:
    print "You need to have the group name in the parameter"
    exit(0)
category = sys.argv[1]
path = sys.argv[2]

print "Category " + category + " will calculated"

output_file = open(path + "/" + category + ".average", "w")
output_file.write("Mean,randomWalkErr,arimaErr,mlpErr,rnnErr\n")
lines = []
count = 0
with open(path + "/" + category + ".info", 'r') as f:
    for line in f.readlines():
        if count == 0:
            count = count + 1
            continue

        if len(line.strip()) == 0:
            continue

        productId, mean, randomWalkErr, arimaErr, mlpErr, rnnErr = line.strip().split(',')
        lines.append((productId, mean, randomWalkErr, arimaErr, mlpErr, rnnErr))
        count = count + 1
    for i in range(1, 6):
        output_file.write(repr(calculateMeanForError(column(lines, i))));
        if i != 5:
            output_file.write(",");
