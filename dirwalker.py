#!/usr/bin/env python

import os
import sys

inDir = sys.argv[1]
dirPath = os.path.abspath(inDir)

pathArray = []

for (path, dirnames, filenames) in os.walk(dirPath):
	pathArray.extend(os.path.join(path, name) for name in filenames)

for path in pathArray:
	print path
