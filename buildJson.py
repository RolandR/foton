#!/usr/bin/env python3

import sys
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
import PIL.ExifTags
import json
import pprint

def humanReadableSize(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1000.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1000.0
    return "%.1f%s%s" % (num, 'Y', suffix)

pp = pprint.PrettyPrinter()

thumbSize = "300"
thumbDirectory = "thumbs/"
zipDirectory = "zip/"

sizes = [800, 1200, 1600, 2000]

indexHTML = ""
figure = ""

with open("index.html", 'r') as indexFile:
	indexHTML = indexFile.read()
	
with open("figure.html", 'r') as figureFile:
	figure = figureFile.read()

path = sys.argv[1]
files = [f for f in sorted(listdir(path)) if isfile(join(path, f))]

if not os.path.isdir(path+thumbDirectory):
	os.system("mkdir "+path+thumbDirectory)

for size in sizes:
	directory = "px"+str(size)+"/"
	if not os.path.isdir(path+directory):
		os.system("mkdir "+path+directory)

if not os.path.isdir(path+zipDirectory):
	os.system("mkdir "+path+zipDirectory)

zipfile = "italy.zip"

if not os.path.isfile(path+zipDirectory+zipfile):
	print("Creating zip file")
	os.system("zip "+path+zipDirectory+zipfile+" "+path+"*.JPG")
else:
	print("Skipping zip file")

zipSize = os.path.getsize(path+zipDirectory+zipfile)
zipSize = humanReadableSize(zipSize)

indexHTML = indexHTML.replace("$ARCHIVESIZE",zipSize);
indexHTML = indexHTML.replace("$ARCHIVE", path+zipDirectory+zipfile);

jsonString = "var metadata = {\n"
jsonString += "\tpath:\""+path+"\",\n"
jsonString += "\timages: [\n"

outFigures = ""

for index, file in enumerate(files):
	if(os.path.isfile("./"+path+thumbDirectory+file)):
		print("["+str(index+1).zfill(len(str(len(files))))+"/"+str(len(files))+"] Skipping "+file+": Thumbnail exists")
	else:
		sys.stdout.write("["+str(index+1).zfill(len(str(len(files))))+"/"+str(len(files))+"] Converting "+file)
		sys.stdout.write(".")
		sys.stdout.flush()
		cmd = "convert "+path+file+" -auto-orient -quality 80 -strip -interlace Plane -resize "+thumbSize+"x"+thumbSize+" "+path+thumbDirectory+file
		os.system(cmd);

		for size in sizes:
			sys.stdout.write('.')
			sys.stdout.flush()
			directory = "px"+str(size)+"/"
			cmd = "convert "+path+file+" -auto-orient -quality 90 -strip -interlace Plane -resize "+str(size)+"x"+str(size)+" "+path+directory+file
			os.system(cmd);

		print();

	img = PIL.Image.open(path+file)
	exif = {}
	
	size = os.path.getsize(path+file)
	size = humanReadableSize(size)

	for k, v in img._getexif().items():
		if k in PIL.ExifTags.TAGS and PIL.ExifTags.TAGS[k] != "MakerNote" and str(v)[0] != "b" and str(v)[0] != "{":
			exif[PIL.ExifTags.TAGS[k]] = v
	
	jsonString += "\t\t{\n"
	jsonString += "\t\t\tfile: \""+file+"\",\n"
	jsonString += "\t\t\tsize: \""+size+"\",\n"
	jsonString += "\t\t\texif:"+pp.pformat(exif)+"\n"
	jsonString += "\t\t}\n"
	if index != len(files)-1:
		jsonString += ","
	jsonString += "\n"

	im = Image.open(path+thumbDirectory+file)
	width, height = im.size

	outFigure = figure;
	outFigure = outFigure.replace("$SRC", path+thumbDirectory+file)
	outFigure = outFigure.replace("$FILE", file)
	outFigure = outFigure.replace("$WIDTH", str(width))
	outFigure = outFigure.replace("$HEIGHT", str(height))
	outFigure = outFigure.replace("$ALT", file)
	outFigures += outFigure

jsonString += "\t]\n};"
with open("metadata.js", 'w') as jsonFile:
	jsonFile.write(jsonString)

indexHTML = indexHTML.replace("$CONTENT", outFigures);

with open("bort.html", 'w') as htmlFile:
	htmlFile.write(indexHTML)

