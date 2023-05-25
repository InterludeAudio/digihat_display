#!/bin/bash

# change to the directory with the python code that is up one directory from this script 
fullpath=`readlink -f $0`
cd `dirname $fullpath`/..

# run display code
python3 display.py
