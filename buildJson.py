#!/usr/bin/env python3

import sys
import os
from os import listdir
from os.path import isfile, join
from PIL import Image

thumbSize = "300"
thumbDirectory = "thumbs/"

indexHTML = ""
figure = ""

with open("index.html", 'r') as indexFile:
	indexHTML = indexFile.read()
	
with open("figure.html", 'r') as figureFile:
	figure = figureFile.read()

path = sys.argv[1]
files = [f for f in sorted(listdir(path)) if isfile(join(path, f))]

os.system("rm -r "+path+thumbDirectory)
os.system("mkdir "+path+thumbDirectory)

json = "{\n"
json += "\tpath: "+path+",\n"
json += "\timages: [\n"

outFigures = ""

for index, file in enumerate(files):
	print("["+str(index+1).zfill(len(str(len(files))))+"/"+str(len(files))+"] Converting "+file)
	cmd = "convert "+path+file+" -auto-orient -quality 80 -strip -interlace Plane -resize "+thumbSize+"x"+thumbSize+" "+path+thumbDirectory+file
	os.system(cmd);
	json += "\t\t"+file
	if index != len(files)-1:
		json += ","
	json += "\n"

	im = Image.open(path+thumbDirectory+file)
	width, height = im.size
	
	outFigure = figure.replace("$SRC", path+thumbDirectory+file)
	outFigure = outFigure.replace("$WIDTH", str(width))
	outFigure = outFigure.replace("$HEIGHT", str(height))
	outFigure = outFigure.replace("$ALT", file)
	outFigures += outFigure

json += "\t]\n}"
with open("foo.json", 'w') as jsonFile:
	jsonFile.write(json)

indexHTML = indexHTML.replace("$CONTENT", outFigures);

with open("bort.html", 'w') as htmlFile:
	htmlFile.write(indexHTML)
