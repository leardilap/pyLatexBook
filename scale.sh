#!/bin/bash

# Name: scale.sh
# Description: scale images in current working directory
# Requires: ImageMagick
# Run: ./scale.sh
# Date: January 2016
# Author: Richard Hill http://retu.be
# Modified by Luis Ardila http://bozica.co

# In this example we're scaling all files with extension .jpg
# to a width of 1800 pixels and saving the scaled version in
# a sub-directory scaled/

source=$(pwd)/photos

#for file in $source*.jpg $source**/*.jpg $source*.JPG $source**/*.JPG # CAPS
#do
for file in $source/*.jpg $source/*.JPG
do
  if [ -f $file ]; then
    echo converting $file
    #identify -ping -format '%w %h' $file
    filename=$(basename $file)
    convert $file -resize 1800x scaled/$filename
  fi
done
	

