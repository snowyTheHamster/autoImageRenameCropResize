import os
import cv2
from PIL import Image
import sys, shutil
import numpy as np

#this method uses the canny method first
#experiment with masking a range of color in the future: https://stackoverflow.com/questions/44588279/find-and-draw-the-largest-contour-in-opencv-on-a-specific-color-python


##Adjust settings below
#Name of the Folders
INPUT_DIR = 'renamed'
CROPPED_DIR = 'cropped'
RESIZED_DIR = 'resized800'
BG_DIR = 'backgrounds'

#Final image dimensions:
WIDTH = 800
HEIGHT = 800

#Final Image Paddings:
MARGIN_LEFT = 30
MARGIN_RIGHT = 30
MARGIN_BOTTOM = 260

#Threshold Settings
CANNY_MIN = 15
CANNY_MAX = 30

#Products Margins within Rectangle
LEFT = 10
TOP = 10
RIGHT = 0
BOTTOM = 10

#Fill Color Outside Contour
FILL_COLOR = [255, 255, 255] # any BGR color value to fill with
MASK_VALUE = 255 # 1 channel white (can be any non-zero uint8 value)


def crop(file):
    #reading the image 
    image = cv2.imread(file)
    edged = cv2.Canny(image, CANNY_MIN, CANNY_MAX)


    # #applying closing function
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 13))
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
    cropped_image = image[y:y+h, x:x+w]

    # Save image to output dir
    file_name, file_ext = os.path.splitext(file)
    output_file_name = os.path.basename(file_name) + '' + file_ext # change cropped image names here
    cv2.imwrite(CROPPED_DIR + '/' + output_file_name, cropped_image)
    print(f'Saved image to . . . {CROPPED_DIR} folder')


#START CROPPING
image_exts = [ '.jpg', '.jpeg', '.png', '.tif' ]

# Create output directory, if doesn't exist
try:
    os.stat(CROPPED_DIR)
except:
    os.mkdir(CROPPED_DIR)

# Iterate over working directory
directory = os.path.dirname(os.path.realpath(sys.argv[0]))
for subdir, dirs, files in os.walk(INPUT_DIR):
    for filename in files:
        if filename.find('.jpg') > 0:   # checks the file extension
            subdirectoryPath = os.path.relpath(subdir, directory)
            filePath = os.path.join(subdirectoryPath, filename)

            file_path = os.path.join(INPUT_DIR, filename)
            file_name, file_ext = os.path.splitext(file_path)

            # Check if file is an image file
            if file_ext not in image_exts:
                print("Skipping " + filename + " (not a supported image file)")
                continue
            else:
                print("Cropping " + filename + "...")
                crop(INPUT_DIR + '/' + filename)


#USE OPENCV with COLOR FILTER IN FUTURE
#https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
#https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv
#START RESIZING
desired_size = (WIDTH - MARGIN_LEFT - MARGIN_RIGHT, HEIGHT - MARGIN_BOTTOM)

for subdir, dirs, files in os.walk(f'./{CROPPED_DIR}'):
    for filename in files:
        if filename.find('.jpg') > 0:
            subdirectoryPath = os.path.relpath(subdir, directory)
            filePath = os.path.join(subdirectoryPath, filename)
            i = Image.open(f'./{CROPPED_DIR}/{filename}')
            fn, fext = os.path.splitext(filename)
            old_size = i.size
            ratio = min([float(desired_size[0])/old_size[0], float(desired_size[1])/old_size[1]])
            new_size = tuple([int(x*ratio) for x in old_size])
            im = i.resize(new_size, Image.ANTIALIAS)
            new_im = Image.open(f'{BG_DIR}/bg-fff-800x800.jpg')
            new_im.paste(im, ((WIDTH - new_size[0]) // 2, HEIGHT - new_size[1] - MARGIN_BOTTOM))
            print(f'Resizing {filename}...')

            try:
                os.stat('./' + RESIZED_DIR)
            except:
                os.mkdir('./' + RESIZED_DIR)

            print("Saving " + filename + " to " + RESIZED_DIR + " folder")
            new_im.save(f'./{RESIZED_DIR}/{fn}{fext}')