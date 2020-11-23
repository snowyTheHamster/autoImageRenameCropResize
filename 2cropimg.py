import traceback
import os
import cv2
from PIL import Image
import sys, shutil
import numpy as np
import PySimpleGUI as sg

image_exts = [ '.jpg', '.jpeg' ]

def cropitup(mode="duel"):
    folders_to_crop = [INPUT_DIR, ORIGINAL_DIR]
    cropped_save_folders = [CROPPED_DIR, CROPPED_DIR_KAGE]

    # Iterate over working directory
    for crop_folder, crop_save in zip(folders_to_crop, cropped_save_folders):
        count = 0
        for _, _, files in os.walk(INPUT_DIR):
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
                    x = x - MLEFT
                    y = y - MTOP
                    w = w + MLEFT + MRIGHT
                    h = h + MTOP + MBOTTOM

                    # draw the biggest contour (c) in white(255) with 1px border
                    image = cv2.rectangle(image,(x,y),(x+w,y+h),(255, 255, 255), 1)
                    
                    # Select which Images to apply changes to
                    original_image = cv2.imread(crop_folder +'/'+ filename) # Apply crops to images in INPUT_DIR
                
                    # crop the image
                    cropped_image = original_image[y:y+h, x:x+w]

                    # Save image to output dir
                    cv2.imwrite(crop_save +'/'+ output_file_name, cropped_image)

                    print(f'{count}/{file_count} Cropping {filename}... done.')

        # If Original Images Folder not selected, dont process second time
        if mode == 'single':
            break


layout = [
    [sg.Text('Original Images folder (Optional):')],
    [sg.Input(key='_ORIGINAL_IMG_'), sg.FolderBrowse()],
    [sg.Text('Bg removed Images folder:')],
    [sg.Input(key='_IN_IMG_'), sg.FolderBrowse()],
    [sg.Text('Output folder:')],
    [sg.Input(key='_OUT_IMG_'), sg.FolderBrowse()],
    [sg.Text('--- Threshold Values ---')],
    [sg.Text('Min Value:'), sg.Slider(key='_MIN_VALUE_', range=(0,255), default_value=210, size=(35,15), orientation='horizontal')],
    [sg.Text('Max Value:'), sg.Slider(key='_MAX_VALUE_', range=(0,255), default_value=200, size=(35,15), orientation='horizontal')],
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
            ORIGINAL_DIR = values['_ORIGINAL_IMG_']
            INPUT_DIR = values['_IN_IMG_']
            OUTPUT_DIR = values['_OUT_IMG_']
            CROPPED_DIR = os.path.join(OUTPUT_DIR, '2_cropped')
            CROPPED_DIR_KAGE = os.path.join(OUTPUT_DIR, '2_cropped_helper')

            MIN_VAL = int(values['_MIN_VALUE_'])
            MAX_VAL = int(values['_MAX_VALUE_'])

            MTOP = int(values['_MARGIN_TOP_'])
            MRIGHT = int(values['_MARGIN_RIGHT_'])
            MBOTTOM = int(values['_MARGIN_BOTTOM_'])
            MLEFT = int(values['_MARGIN_LEFT_'])


            if INPUT_DIR == '' or OUTPUT_DIR == '':
                print('please specify folders')
            elif OUTPUT_DIR == INPUT_DIR:
                print('Output Folder cannot be same as the Input Folder')
            elif os.listdir(OUTPUT_DIR) :
                print('Output Folder must be Empty')
            else:
                try:
                    shutil.rmtree(CROPPED_DIR, ignore_errors=True)
                    shutil.rmtree(CROPPED_DIR_KAGE, ignore_errors=True)
                    os.mkdir(CROPPED_DIR)
                    os.mkdir(CROPPED_DIR_KAGE)
                except:
                    print('directory already exists')

                # if Original Images folder empty
                if ORIGINAL_DIR == '':
                    cropitup("single") # run once
                else:
                    cropitup() # run twice


except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened. Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)