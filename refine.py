import os
import cv2
from PIL import Image
import sys, shutil
import numpy as np

RESIZED_DIR = 'resized800'
REFINED_DIR = 'testrefined'

LEFT = 10
TOP = 10
RIGHT = 10
BOTTOM = 10

#Threshold Settings
CANNY_MIN = 10
CANNY_MAX = 30

#Fill Color Outside Contour
FILL_COLOR = [255, 255, 255] # any BGR color value to fill with
MASK_VALUE = 255 # 1 channel white (can be any non-zero uint8 value)


def refine(file):
    #reading the image 
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edged = cv2.Canny(gray, CANNY_MIN, CANNY_MAX)

    # #applying closing function
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    #finding_contours 
    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #find the biggest contour
    c = max(cnts, key = cv2.contourArea)

    #place c back in a list
    list_c = [ np.array( c ) ] 

    ##FILL OUTSIDE OF COUTOUR WITH COLOR
    stencil = np.zeros(image.shape[:-1]).astype(np.uint8)
    cv2.fillPoly(stencil, list_c, MASK_VALUE)
    sel = stencil != MASK_VALUE # select everything that is not MASK_VALUE
    image[sel] = FILL_COLOR # and fill it with FILL_COLOR

    #MAKE RECTANGLE & CROP
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
    # cropped_image = image[y:y+h, x:x+w]


    # Save image to output dir
    file_name, file_ext = os.path.splitext(file)
    output_file_name = os.path.basename(file_name) + '' + file_ext # change cropped image names here
    cv2.imwrite(REFINED_DIR + '/' + output_file_name, image)
    print(f'Saved image to . . . {REFINED_DIR} folder')


# Create refined directory, if doesn't exist
try:
    os.stat(REFINED_DIR)
except:
    os.mkdir(REFINED_DIR)

image_exts = [ '.jpg', '.jpeg', '.png', '.tif' ]
# Iterate over working directory
directory = os.path.dirname(os.path.realpath(sys.argv[0]))
for subdir, dirs, files in os.walk(RESIZED_DIR):
    for filename in files:
        if filename.find('.jpg') > 0:   # checks the file extension
            subdirectoryPath = os.path.relpath(subdir, directory)
            filePath = os.path.join(subdirectoryPath, filename)

            file_path = os.path.join(RESIZED_DIR, filename)
            file_name, file_ext = os.path.splitext(file_path)

            # Check if file is an image file
            if file_ext not in image_exts:
                print("Skipping " + filename + " (not a supported image file)")
                continue
            else:
                print("Refining " + filename + "...")
                refine(RESIZED_DIR + '/' + filename)
