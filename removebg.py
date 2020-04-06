import os
import cv2
from PIL import Image
import sys, shutil
import numpy as np

INPUT_DIR = 'testin'
TESTOUT_DIR = 'testout'

FILL_COLOR = [255, 255, 255] # any BGR color value to fill with
MASK_VALUE = 255 # 1 channel white (can be any non-zero uint8 value)

LEFT = 10
TOP = 10
RIGHT = 10
BOTTOM = 10

MIN_VAL = 200
MAX_VAL = 10

image_exts = [ '.jpg', '.jpeg', '.png', '.tif' ]

# Iterate over working directory
directory = os.path.dirname(os.path.realpath(sys.argv[0]))
for subdir, dirs, files in os.walk(INPUT_DIR):
    for filename in files:
        file_path = os.path.join(INPUT_DIR, filename)
        file_name, file_ext = os.path.splitext(file_path)
        output_file_name = os.path.basename(file_name) + '' + file_ext # change cropped image names here

        if file_ext not in image_exts:
            print("Skipping " + filename + " (not a supported image file)")
            continue

        else:
            subdirectoryPath = os.path.relpath(subdir, directory)
            filePath = os.path.join(subdirectoryPath, filename)

            if os.path.isfile(TESTOUT_DIR +'/'+ output_file_name):
                print(f'{output_file_name} exists; skipping')
            
            else:
                print("Processing " + filename + "...")

                image = cv2.imread(INPUT_DIR+'/'+filename)
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                # ret, thresh = cv2.threshold(gray, MIN_VAL, MAX_VAL, cv2.THRESH_BINARY)
                ret, thresh = cv2.threshold(gray, MIN_VAL, MAX_VAL, cv2.THRESH_BINARY_INV)
                # ret, thresh = cv2.threshold(gray, MIN_VAL, MAX_VAL, cv2.THRESH_TRUNC)
                # ret, thresh = cv2.threshold(gray, MIN_VAL, MAX_VAL, cv2.THRESH_TOZERO)
                # ret, thresh = cv2.threshold(gray, MIN_VAL, MAX_VAL, cv2.THRESH_TOZERO_INV)

                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13)) # CHANGE BETWEEN MORPH_RECT & MORPH_ELLIPSE; Also tweak last parameter(x, x)
                # morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel) # CHANGE BETWEEN MORPH_CLOSE, MORPH_OPEN, MORPH_DILATE & MORPH_ERODE; Also change between thresh1 - thresh5
                # morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel) # CHANGE BETWEEN MORPH_CLOSE, MORPH_OPEN, MORPH_DILATE & MORPH_ERODE; Also change between thresh1 - thresh5
                morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel) # CHANGE BETWEEN MORPH_CLOSE, MORPH_OPEN, MORPH_DILATE & MORPH_ERODE; Also change between thresh1 - thresh5
                # morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_ERODE, kernel) # CHANGE BETWEEN MORPH_CLOSE, MORPH_OPEN, MORPH_DILATE & MORPH_ERODE; Also change between thresh1 - thresh5

                (cnts, _) = cv2.findContours(morphchoice.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                c = max(cnts, key = cv2.contourArea)

                list_c = [ np.array( c ) ]

                stencil = np.zeros(image.shape[:-1]).astype(np.uint8)
                cv2.fillPoly(stencil, list_c, MASK_VALUE)
                sel = stencil != MASK_VALUE # select everything that is not MASK_VALUE
                image[sel] = FILL_COLOR # and fill it with FILL_COLOR

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

                # file_name, file_ext = os.path.splitext(filename)
                # output_file_name = os.path.basename(file_name) + '' + file_ext # change cropped image names here
                cv2.imwrite(TESTOUT_DIR +'/'+ output_file_name, image)

