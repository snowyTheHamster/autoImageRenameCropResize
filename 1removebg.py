import traceback
import os
import cv2
from PIL import Image
import numpy as np
import PySimpleGUI as sg

image_exts = [ '.jpg', '.jpeg' ]

def removebg():

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
                    print(f'{output_file_name} exists; skipping')
                else:
                    print(f'{count}/{file_count} Removing BG from {filename}...')

                    ###
                    # FIRST ITERATION OF THE IMAGE PROCESS
                    image = cv2.imread(INPUT_DIR +'/'+filename)
                    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                    blurred = cv2.bilateralFilter(gray, 6, 231, 231)

                    #PLAN B: Canny
                    thresh = cv2.Canny(blurred, 2, 6)

                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (77, 77)) # options: MORPH_RECT,MORPH_ELLIPSE; Also tweak last parameter(x, x)
                    morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel) # options: MORPH_CLOSE,MORPH_OPEN,MORPH_DILATE,MORPH_ERODE
                    (cnts, _) = cv2.findContours(morphchoice.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # finding_contours
                    
                    #find the biggest contour
                    c = max(cnts, key = cv2.contourArea)
                    
                    #place c back in a list
                    list_c = [ np.array( c ) ]

                    #FILL OUTSIDE OF COUTOUR WITH COLOR
                    stencil = np.zeros(image.shape[:-1]).astype(np.uint8)
                    cv2.fillPoly(stencil, list_c, MASK_VALUE)
                    sel = stencil != MASK_VALUE # select everything that is not MASK_VALUE
                    image[sel] = FILL_COLOR # and fill it with FILL_COLOR

                    ###
                    # SECOND ITERATION OF THE IMAGE PROCESS
                    image2 = image
                    gray = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)
                    blurred = cv2.bilateralFilter(gray, 6, 131, 131)

                    #PLAN A: threshold
                    ret, thresh = cv2.threshold(blurred, MIN_VALUE, MAX_VALUE, cv2.THRESH_BINARY_INV) # options: THRESH_BINARY,THRESH_BINARY_INV,THRESH_TRUNC,THRESH_TOZERO,THRESH_TOZERO_INV

                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)) # options: MORPH_RECT,MORPH_ELLIPSE; Also tweak last parameter(x, x)
                    morphchoice = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel) # options: MORPH_CLOSE,MORPH_OPEN,MORPH_DILATE,MORPH_ERODE
                    (cnts, _) = cv2.findContours(morphchoice.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # finding_contours

                    #find the biggest contour
                    c = max(cnts, key = cv2.contourArea)
                    
                    #place c back in a list
                    list_c = [ np.array( c ) ]

                    #FILL OUTSIDE OF COUTOUR WITH COLOR
                    stencil = np.zeros(image2.shape[:-1]).astype(np.uint8)
                    cv2.fillPoly(stencil, list_c, MASK_VALUE)
                    sel = stencil != MASK_VALUE # select everything that is not MASK_VALUE
                    image2[sel] = FILL_COLOR # and fill it with FILL_COLOR

                    # Save image to output dir
                    cv2.imwrite(OUTPUT_DIR +'/'+ output_file_name, image2)
        print('done.')


layout = [
    [sg.Text('Input folder with jpgs:')],
    [sg.Input(key='_IN_IMG_'), sg.FolderBrowse()],
    [sg.Text('Output folder:')],
    [sg.Input(key='_OUT_IMG_'), sg.FolderBrowse()],
    [sg.Text('--- Threshold Values ---')],
    [sg.Text('Min Value:'), sg.Slider(key='_MIN_VALUE_', range=(0,255), default_value=200, size=(35,15), orientation='horizontal')],
    [sg.Text('Max Value:'), sg.Slider(key='_MAX_VALUE_', range=(0,255), default_value=10, size=(35,15), orientation='horizontal')],
    [sg.Text('Mask Value:'), sg.Slider(key='_MASK_VALUE_', range=(0,255), default_value=255, size=(35,15), orientation='horizontal')],
    [sg.Text('--- Background Fill Value ---')],
    [sg.Text('B:'), sg.Slider(key='_FILL_VALUE1_', range=(0,255), default_value=255, size=(35,15), orientation='horizontal')],
    [sg.Text('G:'), sg.Slider(key='_FILL_VALUE2_', range=(0,255), default_value=255, size=(35,15), orientation='horizontal')],
    [sg.Text('R:'), sg.Slider(key='_FILL_VALUE3_', range=(0,255), default_value=255, size=(35,15), orientation='horizontal')],
    [sg.Text('')],
    [sg.Button("Process", size=(10, 1), bind_return_key=True, key='_PROCESS_')],
    [sg.Output(size=(60, 10))],
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
            MIN_VALUE = int(values['_MIN_VALUE_'])
            MAX_VALUE = int(values['_MAX_VALUE_'])
            MASK_VALUE = int(values['_MASK_VALUE_'])
            FILL_1 = int(values['_FILL_VALUE1_'])
            FILL_2 = int(values['_FILL_VALUE2_'])
            FILL_3 = int(values['_FILL_VALUE3_'])
            FILL_COLOR = [FILL_1, FILL_2, FILL_3]

            if INPUT_DIR == '' or OUTPUT_DIR == '' :
                print('please specify folders')
            elif OUTPUT_DIR == INPUT_DIR:
                print('Output Folder cannot be same as the Input Folder')
            elif os.listdir(OUTPUT_DIR) :
                print('Output Folder must be Empty')
            else:
                removebg()

except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened.  Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)