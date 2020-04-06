import os
import cv2
from PIL import Image
import sys, shutil
import numpy as np


##Adjust settings below
INPUT_DIR = '2_bg_removed'
OUTPUT_DIR = '3_cropped'
MIN_VAL = 210
MAX_VAL = 200

image_exts = [ '.jpg', '.jpeg', '.png', '.tif' ]

#Products Margins within Rectangle
LEFT = 0
TOP = 0
RIGHT = 0
BOTTOM = 0

# Iterate over working directory
directory = os.path.dirname(os.path.realpath(sys.argv[0]))
for subdir, dirs, files in os.walk(INPUT_DIR):
    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        file_name, file_ext = os.path.splitext(file_path)
        output_file_name = os.path.basename(file_name) + file_ext # save imagename (change ext if you want)

        if file_ext not in image_exts:
            print("Skipping " + filename + " (not a supported image file)")
            continue

        else:
            if os.path.isfile(OUTPUT_DIR +'/'+ output_file_name):
                print(f'{output_file_name} exists; skipping')
                
            else:
                print("Processing " + filename + "...")

                image = cv2.imread(INPUT_DIR+'/'+filename)
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                ret, thresh = cv2.threshold(gray, MIN_VAL, MAX_VAL, cv2.THRESH_BINARY_INV) # options: THRESH_BINARY,THRESH_BINARY_INV,THRESH_TRUNC,THRESH_TOZERO,THRESH_TOZERO_INV

                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)) # options: MORPH_RECT,MORPH_ELLIPSE; Also tweak last parameter(x, x)
                morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel) # options: MORPH_CLOSE,MORPH_OPEN,MORPH_DILATE,MORPH_ERODE
                
                #finding_contours 
                (cnts, _) = cv2.findContours(morphchoice.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                #find the biggest contour
                c = max(cnts, key = cv2.contourArea)
                
                #place c back in a list
                list_c = [ np.array( c ) ]

                # Make a rectangle from the largest coutour
                x,y,w,h = cv2.boundingRect(c)
                # Set margins for the Rectangle to prevent clipping of product
                x = x - LEFT
                y = y - TOP
                w = w + RIGHT
                h = h + BOTTOM

                # draw the biggest contour (c) in white(255) with 1px border
                image = cv2.rectangle(image,(x,y),(x+w,y+h),(255, 255, 255), 1)
                # crop the image
                cropped_image = image[y:y+h, x:x+w]

                # Save image to output dir
                cv2.imwrite(OUTPUT_DIR +'/'+ output_file_name, cropped_image)
                print(f'Saved image to . . . {OUTPUT_DIR} folder')
