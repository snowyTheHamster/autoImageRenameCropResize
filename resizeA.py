import os
import cv2
from PIL import Image
import sys, shutil
import numpy as np


##Adjust settings below
INPUT_DIR = '2_cropped'
OUTPUT_DIR = '3_resized'

#Final image dimensions:
WIDTH = 800
HEIGHT = 800

#Final Image Paddings:
MARGIN_LEFT = 30
MARGIN_RIGHT = 30
MARGIN_BOTTOM = 260

desired_size = (WIDTH - MARGIN_LEFT - MARGIN_RIGHT, HEIGHT - MARGIN_BOTTOM)

image_exts = [ '.jpg', '.jpeg', '.png', '.tif' ]

# Iterate over working directory
# directory = os.path.dirname(os.path.realpath(sys.argv[0]))
count=0
for subdir, dirs, files in os.walk(INPUT_DIR):
    file_count = len(files)
    for filename in files:
        count +=1
        file_path = os.path.join(INPUT_DIR, filename)
        file_name, file_ext = os.path.splitext(file_path)
        output_file_name = os.path.basename(file_name) + file_ext # save imagename (change ext if you want)

        if file_ext not in image_exts:
            print("Skipping " + filename + " (not a supported image file)")
            count -=1
            file_count -= 1
            continue

        else:
            if os.path.isfile(OUTPUT_DIR +'/'+ output_file_name):
                print(f'{output_file_name} exists; skipping')
                
            else:
                print(f'{count}/{file_count} processing {filename}...')

                i = Image.open(f'./{INPUT_DIR}/{filename}')
                fn, fext = os.path.splitext(filename)
                old_size = i.size
                ratio = min([float(desired_size[0])/old_size[0], float(desired_size[1])/old_size[1]])
                new_size = tuple([int(x*ratio) for x in old_size])
                im = i.resize(new_size, Image.ANTIALIAS)
                new_im = Image.new('RGB', size = (WIDTH, HEIGHT), color = (255, 255, 255)) #generate bg image
                new_im.paste(im, ((WIDTH - new_size[0]) // 2, HEIGHT - new_size[1] - MARGIN_BOTTOM))

                # Create output directory if it don't exist
                try:
                    os.stat('./' + OUTPUT_DIR)
                except:
                    os.mkdir('./' + OUTPUT_DIR)
                
                print("Saving " + filename + " to " + OUTPUT_DIR + " folder")
                new_im.save(f'./{OUTPUT_DIR}/{fn}{fext}')