import traceback
import os
import cv2
from PIL import Image
import sys, shutil
import numpy as np
import PySimpleGUI as sg

image_exts = [ '.jpg', '.jpeg' ]


def folder_init():
    # create temp folders
    try:
        os.mkdir(CROPPED_DIR)
        os.mkdir(CROPPED_DIR_KAGE)
    except:
        print('directory already exists')


def cropitup():
    cropped_save_folders = [CROPPED_DIR_KAGE, CROPPED_DIR]

    MIN_VAL = 210
    MAX_VAL = 200

    #Products Margins within Rectangle
    LEFT = 0 + MLEFT
    TOP = 200 + MTOP
    RIGHT = 0 + MRIGHT
    BOTTOM = 220

    # Iterate over working directory
    for crop_save in cropped_save_folders:
        count = 0
        for _, _, files in os.walk(REFERENCE_DIR):
            file_count = len(files)
            for filename in files:
                count +=1
                file_path = os.path.join(REFERENCE_DIR, filename)
                file_name, file_ext = os.path.splitext(file_path)
                output_file_name = os.path.basename(file_name) + file_ext # save imagename (change ext if you want)

                if file_ext not in image_exts:
                    print("Skipping " + filename + " (not a supported image file)")
                    count -=1
                    file_count -= 1
                    continue

                else:
                    print(f'{count}/{file_count} Cropping {filename}...')

                    image = cv2.imread(REFERENCE_DIR+'/'+filename)
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
                    
                    # Select which Images to apply changes to
                    original_image = cv2.imread(INPUT_DIR +'/'+ filename) # Apply crops to images in INPUT_DIR
                
                    # crop the image
                    cropped_image = original_image[y:y+h, x:x+w]

                    # Save image to output dir
                    cv2.imwrite(crop_save +'/'+ output_file_name, cropped_image)


layout = [
    [sg.Text('Input folder:')],
    [sg.Input(key='_IN_IMG_'), sg.FolderBrowse()],
    [sg.Text('Output folder:')],
    [sg.Input(key='_OUT_IMG_'), sg.FolderBrowse()],
    [sg.Text('')],
    [sg.Text('Additional Margins (px)')],
    [sg.Text('Top:'), sg.InputText(0, key='_MARGIN_TOP_', size=(5,1)), sg.Text('Right:'), sg.InputText(0, key='_MARGIN_RIGHT_', size=(5,1)), sg.Text('Bottom:'), sg.InputText(0, key='_MARGIN_BOTTOM_', size=(5,1)), sg.Text('Left:'), sg.InputText(0, key='_MARGIN_LEFT_', size=(5,1))],
    [sg.Button("Process", size=(10, 1), bind_return_key=True, key='_PROCESS_')],
    [sg.Output(size=(60, 10))],
]

window: object = sg.Window('Bulk Image Cropper', layout, element_justification='left')

try:
    while True:
        event, values = window.read()
        if event is None:
            break
        if event == '_PROCESS_':
            INPUT_DIR = values['_IN_IMG_']
            OUTPUT_DIR = values['_OUT_IMG_']
            CROPPED_DIR = os.path.join(OUTPUT_DIR, '2_cropped')
            CROPPED_DIR_KAGE = os.path.join(OUTPUT_DIR, '2_cropped_helper')

            MTOP = int(values['_MARGIN_TOP_'])
            MRIGHT = int(values['_MARGIN_RIGHT_'])
            MBOTTOM = int(values['_MARGIN_BOTTOM_'])
            MLEFT = int(values['_MARGIN_LEFT_'])


            if INPUT_DIR == '' or OUTPUT_DIR == '':
                print('please specify folders')
            elif OUTPUT_DIR == INPUT_DIR:
                print('Output Folder cannot be same as the Input Folder')
            elif os.listdir(CROPPED_DIR) :
                print('2_cropped Folder must be Empty')
            elif os.listdir(CROPPED_DIR_KAGE) :
                print('2_cropped_helper Folder must be Empty')
            else:
                folder_init()
                cropitup()

except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened. Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)