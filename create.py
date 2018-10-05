#!/usr/bin/env python

# Name: create.py
# Description: Generate images latex for all images defined by 'files' below
# Run: python create.py > photos.tex
# Date: January 2016
# Author: Richard Hill http://retu.be
# Modified by: Luis Ardila http://bozica.co

import glob
import os,sys
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import json

# Get all images (.JPG and .jpg in this example)
files = glob.glob(os.getcwd() + "/scaled/*.JPG")
files.extend(glob.glob(os.getcwd() + "/scaled/*.jpg"))


# Returns value of specified exif field.
def get_exif_value(exif, field) :
	for (k,v) in exif.iteritems():
		if TAGS.get(k) == field:
        		return v

def get_comparator(filepath):
	return get_timestamp(get_exif_data(filepath))

def get_exif_data(filepath):
	return Image.open(filepath)._getexif();

def get_timestamp(exif):
	dt = get_exif_value(exif,"DateTimeOriginal")	
	return datetime.strptime(dt, '%Y:%m:%d %H:%M:%S')

# Gets name of image from full path. Escapes underscores for latex. 
def get_filename(filepath):
	return (os.path.basename(filepath)).replace("_","\_");

# Prints the latex for each image. Images have a black border and caption
# detailing the file name and date taken (as determined by exif data)
def get_latex(filepath):

	exif = get_exif_data(filepath)
	do = get_timestamp(exif)

	print '\\begin{figure}[ht!]'
	print '\\centering'
	print "{%"
	print "\\setlength{\\fboxsep}{0pt}%"
	print "\\setlength{\\fboxrule}{0pt}%"
	print "\\fbox{\\includegraphics[height=100mm]{" + filepath + "}}%"
	print "}%"	
	print '\\vspace{9 mm}\n'
	print '\\caption{' + '\\texttt{' + captions[get_filename(filepath).split('.')[0]] + ' - }' + ' ' + do.strftime('%d') + ' ' + do.strftime('%B') + ' ' + do.strftime('%Y') + '}'
	print '\\end{figure}\n'
	return;

# Sort the images chronologically
files = sorted(files, key=get_comparator)

# Get captions
try:
    captions = json.load(open(os.getcwd() + "/scaled/captions.json"))
except: 
    captions = {}
    count = 1
    for filepath in files:
	    captions[get_filename(filepath).split('.')[0]] = "sample caption "+ str(count)
	    count = count + 1

    json.dump(captions, open(os.getcwd() + "/scaled/captions.json", 'w'), indent=4)

# Loop over images and print latex for each
count = 0
for filepath in files:
	count = count + 1
	get_latex(filepath)
	if count % 1 == 0:
		print "\\newpage\n"
	else:
		print '\\vspace{8 mm}\n'
	

