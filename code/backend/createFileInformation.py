#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# createfileInformation.py argument



import os
import string
import sys


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


def callModel1():
    return


def callModel2():
    return


def callModel3():
    return


def callModel4():
    return


# START
if len(sys.argv) != 2:
    print "You need to have the group name in the parameter"
    exit(0)

# Get the groupname form the parameters
output_file = open(sys.argv[1] + ".info", "w");
output_file.write("Product,Mean\n")

for file in os.listdir('.'):
    if os.path.isfile(file):
        if file.endswith(".full"):
            index = string.find(file, ".")
            filename = file[0:index]

            output_file.write(filename)
            output_file.write(",")
            output_file.write(repr(calulateMean(file)))

            # model 1

            # output_file.write(",")
            # model 2

            # output_file.write(",")
            # model 3

            # output_file.write(",")
            # model 4




            output_file.write("\n")
            continue
        else:
            continue
