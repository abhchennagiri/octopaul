#!/bin/bash
FILES=dat/*


for f in FILES 
do 
	for d in f/* 
	do
	
	done	
done

do
  echo "Processing $f file..."
	if echo "basename $f" | grep '.csv'; then
		python createFileInformation.py $f
	fi
	
done

f =find dat -name "*.csv"
