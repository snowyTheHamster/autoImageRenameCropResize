import traceback
import os
import cv2
from PIL import Image
import numpy as np
import PySimpleGUI as sg
import time

image_exts = [ '.jpg', '.jpeg', '.JPG' ]


def removebg(INPUT_DIR, OUTPUT_DIR):

    stime = time.time() # start timer

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
                if os.path.isfile(OUTPUT_DIR +'/'+ output_file_name):
                    print(f'{count}/{file_count} Removing BG from {filename}...')

                    image = cv2.imread(INPUT_DIR +'/'+filename)

                    ###
                    # Grayscale the image then Blur it ith Bilateral Filter
                    image2 = image
                    gray = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)
                    blurred = cv2.bilateralFilter(gray, bf1, bf2, bf3)

                    # Apply Simple Thresholding
                    if values['Radio_1'] == True:
                        ret, thresh = cv2.threshold(blurred, THRESH_VALUE, 10, cv2.THRESH_BINARY)
                    if values['Radio_2'] == True:
                        ret, thresh = cv2.threshold(blurred, THRESH_VALUE, 10, cv2.THRESH_BINARY_INV)

                    # Kernel for Morph below
                    if values['Radio_kernel_1'] == True:
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_1, kernel_2))
                    if values['Radio_kernel_2'] == True:
                        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_1, kernel_2))

                    # Adjust Morph to tweak selection around object
                    if values['Radio_morph_1'] == True:
                        morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
                    if values['Radio_morph_2'] == True:
                        morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                    if values['Radio_morph_3'] == True:
                        morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
                    if values['Radio_morph_4'] == True:
                        morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_ERODE, kernel)

                    (cnts, _) = cv2.findContours(morphchoice.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # finding_contours

                    # Find the biggest contour in image
                    try:
                        c = max(cnts, key = cv2.contourArea)
                    except:
                        print('cant find max contour, skipping this image...')
                        pass
                    
                    # place c back in a list
                    list_c = [ np.array( c ) ]

                    # FILL OUTSIDE OF COUTOUR WITH COLOR
                    stencil = np.zeros(image2.shape[:-1]).astype(np.uint8)
                    cv2.fillPoly(stencil, list_c, 255)
                    sel = stencil != 255 # select everything that is not MASK_VALUE
                    image2[sel] = FILL_COLOR # and fill it with FILL_COLOR

                    # Save and overwrite image in output dir
                    cv2.imwrite(OUTPUT_DIR +'/'+ output_file_name, image2)
                else:
                    # Don't save image if it doesn't already exist in output dir !!
                    print(f'{output_file_name} does not exist; skipping it')

    etime = time.time() #end time
    totaltime = etime - stime
    totaltime = round(totaltime, 1) #round off end time
    print(f'Done Processing in: {totaltime} seconds \n')


layout = [
    [sg.Text('Copy & Paste input files to output files first, then begin process ')],
    [sg.Text('This script only updates existing files in output')],

    [sg.Text('Input folder with jpgs:')],
    [sg.Input(key='_IN_IMG_'), sg.FolderBrowse()],
    [sg.Text('Output folder:')],
    [sg.Input(key='_OUT_IMG_'), sg.FolderBrowse()],
    [sg.Text('--- Bilateral Filter ---')],
    [sg.Text('Diameter:'), sg.InputText(5, key='bf1', size=(5,1)), 
            sg.Text('Sigma Color:'), sg.InputText(131, key='bf2', size=(5,1)), 
            sg.Text('Sigma Space:'), sg.InputText(131, key='bf3', size=(5,1))],

    [sg.Text('--- Simple Thresholding ---')],
    [sg.Text('Threshold Value (1~255):'), sg.InputText(180, key='_THRESH_VALUE_', size=(5,1))],
    [sg.Radio('BINARY', "_RADIO_THRESH_", key='Radio_1'),
            sg.Radio('BINARY_INV', "_RADIO_THRESH_", default=True, key='Radio_2')],

    [sg.Text('--- Morphology ---')],
    [sg.Radio('CLOSE', "_RADIO_morphology_", key='Radio_morph_1'),
            sg.Radio('OPEN', "_RADIO_morphology_", key='Radio_morph_2'),
            sg.Radio('DILATE', "_RADIO_morphology_", default=True, key='Radio_morph_3'),
            sg.Radio('ERODE', "_RADIO_morphology_", key='Radio_morph_4')],

    [sg.Text('--- KERNEL for Morphology ---')],
    [sg.Radio('RECT', "_RADIO_KERNEL_", default=True, key='Radio_kernel_1'),
            sg.Radio('ELLIPSE', "_RADIO_KERNEL_", key='Radio_kernel_2')],
    [sg.Text('Value 1:'), sg.InputText(2, key='_kernel_1_', size=(5,1)),
            sg.Text('Value 2:'), sg.InputText(2, key='_kernel_2_', size=(5,1))],

    [sg.Text('--- BG Fill Color ---')],
    [sg.Text('B:'), sg.Slider(key='_FILL_VALUE1_', range=(0,255), default_value=255, size=(10,15), orientation='horizontal'), 
            sg.Text('G:'), sg.Slider(key='_FILL_VALUE2_', range=(0,255), default_value=255, size=(10,15), orientation='horizontal'),
            sg.Text('R:'), sg.Slider(key='_FILL_VALUE3_', range=(0,255), default_value=255, size=(10,15), orientation='horizontal')],
    [sg.Text('')],
    [sg.Button("Process", size=(10, 1), bind_return_key=True, key='_PROCESS_')],
    [sg.Output(size=(60, 5))],
]

window: object = sg.Window('OpenCV BG Removal', layout, element_justification='left')

try:
    while True:
        event, values = window.read()
        if event is None:
            break

        if event == '_PROCESS_':

            INPUT_DIR = values['_IN_IMG_']
            OUTPUT_DIR = values['_OUT_IMG_']
            
            bf1 = int(values['bf1'])
            bf2 = int(values['bf2'])
            bf3 = int(values['bf3'])

            THRESH_VALUE = int(values['_THRESH_VALUE_'])

            kernel_1 = int(values['_kernel_1_'])
            kernel_2 = int(values['_kernel_2_'])

            FILL_1 = int(values['_FILL_VALUE1_'])
            FILL_2 = int(values['_FILL_VALUE2_'])
            FILL_3 = int(values['_FILL_VALUE3_'])
            FILL_COLOR = [FILL_1, FILL_2, FILL_3]

            if INPUT_DIR == '' or OUTPUT_DIR == '' :
                print('please specify folders')
            elif OUTPUT_DIR == INPUT_DIR:
                print('Output Folder cannot be same as the Input Folder')
            else:
                removebg(INPUT_DIR, OUTPUT_DIR)


except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened.  Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)