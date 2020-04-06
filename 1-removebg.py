import os
import cv2
from PIL import Image
import sys, shutil
import numpy as np

INPUT_DIR = '0_input_images'
TESTOUT_DIR = '1_bg_removed'

FILL_COLOR = [255, 255, 255] # any BGR color value to fill with
MASK_VALUE = 255 # 1 channel white (can be any non-zero uint8 value)

MIN_VAL = 200 #DEFAULT SETTINGS
MAX_VAL = 10

image_exts = [ '.jpg', '.jpeg', '.png', '.tif' ]

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
            if os.path.isfile(TESTOUT_DIR +'/'+ output_file_name):
                print(f'{output_file_name} exists; skipping')
            
            else:
                print("Processing " + filename + "...")

                image = cv2.imread(INPUT_DIR+'/'+filename)
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                #PLAN A SETTINGS
                # ret, thresh = cv2.threshold(gray, MIN_VAL, MAX_VAL, cv2.THRESH_BINARY_INV) # options: THRESH_BINARY,THRESH_BINARY_INV,THRESH_TRUNC,THRESH_TOZERO,THRESH_TOZERO_INV
                # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)) # options: MORPH_RECT,MORPH_ELLIPSE; Also tweak last parameter(x, x)
                # morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel) # options: MORPH_CLOSE,MORPH_OPEN,MORPH_DILATE,MORPH_ERODE
                # (cnts, _) = cv2.findContours(morphchoice.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # finding_contours

                #PLAN B SETTINGS
                edged = cv2.Canny(image, 10, 35)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
                closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
                (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                
                #find the biggest contour
                c = max(cnts, key = cv2.contourArea)
                
                #place c back in a list
                list_c = [ np.array( c ) ]

                #FILL OUTSIDE OF COUTOUR WITH COLOR
                stencil = np.zeros(image.shape[:-1]).astype(np.uint8)
                cv2.fillPoly(stencil, list_c, MASK_VALUE)
                sel = stencil != MASK_VALUE # select everything that is not MASK_VALUE
                image[sel] = FILL_COLOR # and fill it with FILL_COLOR

                # Save image to output dir
                cv2.imwrite(TESTOUT_DIR +'/'+ output_file_name, image)