from pathlib import Path
import os
import shutil
import glob
import csv

# ONLY PUT IMAGES IN THE INPUT FOLDER, watch out for hidden files

locacsv = "list.csv" #csv file name
imgno = 3 # No. of images per model

INPUT_DIR = '3_resized800_b'
OUTPUT_DIR = '4_renamed_b'


f = open(locacsv)
csv_f = csv.reader(f)

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True) # create output folder if it don't exist

for row in csv_f: # per each row in csv file
    last2digit = row[0][-2:] # get last two value from string
    for y in range(imgno): # repeat below loop x number of times
        y = y + 1 # set as 1 instead of 0

        new_img = f'{row[0]}_{last2digit}_{y}.jpg' # final filename we want

        imgs = sorted(os.listdir(INPUT_DIR)) # gets list of images in a directory (add sorted or it won't work on some workstations)
        img_old_path = os.path.join(INPUT_DIR, imgs[0]) # set fullpath of first image in directory
        img_new_path = os.path.join(OUTPUT_DIR, new_img) # set fullpath of image in target directory

        print(f'moving filename: {img_old_path}')
        shutil.move(img_old_path, img_new_path) # moves image and renames it in new target directory