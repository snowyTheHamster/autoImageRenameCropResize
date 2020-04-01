from pathlib import Path
import os
import shutil
import glob
import csv

#PUT THIS SCRIPT, IMAGE DIR & CSV FILE IN THE SAME DIRECTORY
#This script "MOVES" the original images, you must backup your images elsewhere beforehand.

# Input Images folder name
locaimgsdir = "inputimages"
# Input csv file name
locacsv = "list.csv"
# Input how many images per model
imgno = 3
# output folder name
locatargetfolder = "renamed"


locainputdir = os.path.join("." , locaimgsdir)
locaout = os.path.join("." , locatargetfolder)


f = open(locacsv)
csv_f = csv.reader(f)

Path(locaout).mkdir(parents=True, exist_ok=True) # create output folder if it don't exist

for row in csv_f: # per each row in csv file
    last2digit = row[0][-2:] # get last two value from string
    for y in range(imgno): # repeat below loop x number of times
        y = y + 1 # set as 1 instead of 0

        newimg = f'{row[0]}_{last2digit}_{y}_1.jpg' # final filename we want

        imgs = sorted(os.listdir(locainputdir)) # gets list of images in a directory (add sorted or it won't work on some workstations)
        imgoldpath = os.path.join(locainputdir, imgs[0]) # set fullpath of first image in directory
        imgnewpath = os.path.join(locaout, newimg) # set fullpath of image in target directory

        print(f'moving filename: {imgoldpath}')
        shutil.move(imgoldpath, imgnewpath) # moves image and renames it in new target directory