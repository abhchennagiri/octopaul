#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# createfileInformation.py

import csv
import sys
import os


# print sys.argv[0] filename
# print sys.argv[1]
# print sys.argv[2]


def calulateMean():
    mean = 0.0
    lines = []
    with open(sys.argv[1], 'r') as f:
        for line in f.readlines():
            l, name = line.strip().split(',')
            lines.append((l, name))

    # print lines[1]  # touple with files
    # print lines[1][1] #second value is the price
    count = 0
    del lines[0]
    for line in lines:
        count = count + 1
        # print line
        # print line[0]
        mean = mean + float(line[1])
        # print mean
    if count != 0:
        mean = mean / count
    else:
        mean = 0
    # print "mean is "
    return mean


print "start"

output_file = open(os.path.splitext(os.path.basename(sys.argv[1]))[0] + ".info", "w");
output_file.write("product,mean\n")
output_file.write(os.path.splitext(os.path.basename(sys.argv[1]))[0]);
output_file.write(",")
output_file.write(repr(calulateMean()))
# output_file.write("\n")
