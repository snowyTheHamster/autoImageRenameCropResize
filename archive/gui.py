import traceback
import os
import cv2
from PIL import Image
import sys, shutil
import numpy as np
import PySimpleGUI as sg
import csv

image_exts = [ '.jpg', '.jpeg' ]


def folder_init():
    # create temp folders
    try:
        os.mkdir(BG_REMOVED_DIR)
        os.mkdir(CROPPED_DIR)
        os.mkdir(CROPPED_DIR_KAGE)
        os.mkdir(RESIZED_DIR)
        os.mkdir(RESIZED_DIR_KAGE)
        os.mkdir(RENAMED_DIR)
        os.mkdir(RENAMED_DIR_KAGE)
    except:
        print('directory already exists')

def touchitup(mode="live"):
    # bg removal 1 variables
    FILL_COLOR = [255, 255, 255] # any BGR color value to fill with
    MASK_VALUE = 255 # 1 channel white (can be any non-zero uint8 value)
    # bg removal 2 variables
    MIN_VAL = 200 #DEFAULT SETTINGS
    MAX_VAL = 10

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
                if os.path.isfile(BG_REMOVED_DIR +'/'+ output_file_name):
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
                    ret, thresh = cv2.threshold(blurred, MIN_VAL, MAX_VAL, cv2.THRESH_BINARY_INV) # options: THRESH_BINARY,THRESH_BINARY_INV,THRESH_TRUNC,THRESH_TOZERO,THRESH_TOZERO_INV

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
                    cv2.imwrite(BG_REMOVED_DIR +'/'+ output_file_name, image2)

                    if mode == 'test':
                        break

def cropitup(mode="live"):
    REFERENCE_DIR = BG_REMOVED_DIR

    folders_to_crop = [INPUT_DIR, REFERENCE_DIR]
    cropped_save_folders = [CROPPED_DIR_KAGE, CROPPED_DIR]

    MIN_VAL = 210
    MAX_VAL = 200

    #Products Margins within Rectangle
    LEFT = 0 + MLEFT
    TOP = 200 + MTOP
    RIGHT = 0 + MRIGHT
    BOTTOM = 220

    # Iterate over working directory
    # directory = os.path.dirname(os.path.realpath(sys.argv[0]))
    for crop_folder, crop_save in zip(folders_to_crop, cropped_save_folders):
        count = 0
        for _, _, files in os.walk(REFERENCE_DIR):
            file_count = len(files)
            for filename in files:
                count +=1
                file_path = os.path.join(REFERENCE_DIR, filename)
                file_name, file_ext = os.path.splitext(file_path)
                output_file_name = os.path.basename(file_name) + file_ext # save imagename (change ext if you want)

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
                original_image = cv2.imread(crop_folder +'/'+ filename) # Apply crops to images in INPUT_DIR
            
                # crop the image
                cropped_image = original_image[y:y+h, x:x+w]

                # Save image to output dir
                cv2.imwrite(crop_save +'/'+ output_file_name, cropped_image)

                if mode == 'test':
                    break


def resizeitup(mode="live"):
    #Final Image Paddings:
    # MARGIN_LEFT = 30
    # MARGIN_RIGHT = 30
    # MARGIN_BOTTOM = 26
    MARGIN_LEFT = 20
    MARGIN_RIGHT = 20
    MARGIN_BOTTOM = 276 + MBOTTOM

    desired_size = (WIDTH - MARGIN_LEFT - MARGIN_RIGHT, HEIGHT - MARGIN_BOTTOM)

    folders_to_resize = [CROPPED_DIR_KAGE, CROPPED_DIR]
    resized_save_folders = [RESIZED_DIR_KAGE, RESIZED_DIR]

    for resize_folder, resize_save in zip(folders_to_resize, resized_save_folders):
        count = 0
        for _, _, files in os.walk(resize_folder):
            file_count = len(files)
            for filename in files:
                count +=1
                file_path = os.path.join(resize_folder, filename)
                file_name, file_ext = os.path.splitext(file_path)
                output_file_name = os.path.basename(file_name) + file_ext # save imagename (change ext if you want)

                print(f'{count}/{file_count} resizing {filename}...')

                i = Image.open(f'{resize_folder}/{filename}')
                fn, fext = os.path.splitext(filename)
                old_size = i.size
                ratio = min([float(desired_size[0])/old_size[0], float(desired_size[1])/old_size[1]])
                new_size = tuple([int(x*ratio) for x in old_size])
                im = i.resize(new_size, Image.ANTIALIAS)
                new_im = Image.new('RGB', size = (WIDTH, HEIGHT), color = (255, 255, 255)) #generate bg image
                new_im.paste(im, ((WIDTH - new_size[0]) // 2, HEIGHT - new_size[1] - MARGIN_BOTTOM))

                new_im.save(f'{resize_save}/{fn}{fext}')

                if mode == 'test':
                    break


def renameitup(mode="live"):

    folders_to_rename = [RESIZED_DIR_KAGE, RESIZED_DIR]
    renamed_save_folders = [RENAMED_DIR_KAGE, RENAMED_DIR]

    if mode == 'test':
        no_of_imgs = 1
    elif mode =='live':
        no_of_imgs = int(values['_IMG_ANGLES_'])

    for INPUT_DIR, OUTPUT_DIR in zip(folders_to_rename, renamed_save_folders):
        f = open(csvfile)
        csv_f = csv.reader(f)

        for row in csv_f: # per each row in csv file
            for y in range(no_of_imgs): # repeat below loop x number of times
                y = y + 1

                new_img = f'{row[0]}_{y}.jpg' # final filename we want

                imgs = sorted(os.listdir(INPUT_DIR)) # gets list of images in a directory (add sorted or it won't work on some workstations)
                img_old_path = os.path.join(INPUT_DIR, imgs[0]) # set fullpath of first image in directory
                img_new_path = os.path.join(OUTPUT_DIR, new_img) # set fullpath of image in target directory

                print(f'rename and move file to: {img_new_path}')
                shutil.move(img_old_path, img_new_path) # moves image and renames it in new target directory

            if mode == 'test':
                break


def cleanitup():
    # delete all temp folders inside output folder
    try:
        shutil.rmtree(BG_REMOVED_DIR, ignore_errors=True)
        shutil.rmtree(CROPPED_DIR, ignore_errors=True)
        shutil.rmtree(CROPPED_DIR_KAGE, ignore_errors=True)
        shutil.rmtree(RESIZED_DIR, ignore_errors=True)
        shutil.rmtree(RESIZED_DIR_KAGE, ignore_errors=True)
    except:
        print(f'clean up failed to delete one of the temp folders')

    print('Done.')


layout = [
    [sg.Text('Input folder:')],
    [sg.Input(key='_IN_IMG_'), sg.FolderBrowse()],
    [sg.Text('Output folder:')],
    [sg.Input(key='_OUT_IMG_'), sg.FolderBrowse()],
    [sg.Text('')],
    [sg.Text('--- RESIZE FUNCTION ---')],
    [sg.Text('New Width (px):'), sg.InputText(1000, key='_NEW_WIDTH_', size=(5,1))],
    [sg.Text('New Height (px):'), sg.InputText(1000, key='_NEW_HEIGHT_', size=(5,1))],
    [sg.Text('')],
    [sg.Text('--- RENAME FUNCTION--- ')],
    [sg.Text('csv with 1 filename/line:'), sg.Input(key='_RENAME_CSV_'), sg.FileBrowse()],
    [sg.Text('No. per Image:'), sg.InputText(key='_IMG_ANGLES_', size=(5,1))],
    [sg.Text('')],
    [sg.Text('Additional Margins (px)')],
    [sg.Text('Top:'), sg.InputText(0, key='_MARGIN_TOP_', size=(5,1)), sg.Text('Right:'), sg.InputText(0, key='_MARGIN_RIGHT_', size=(5,1)), sg.Text('Bottom:'), sg.InputText(0, key='_MARGIN_BOTTOM_', size=(5,1)), sg.Text('Left:'), sg.InputText(0, key='_MARGIN_LEFT_', size=(5,1))],
    [sg.Button("Test", size=(10, 1), key='_TEST_')],
    [sg.Button("Process", size=(10, 1), bind_return_key=True, key='_PROCESS_')],
    [sg.Output(size=(60, 10))],
]

window: object = sg.Window('Product Photo Auto Retouch (jpg)', layout, element_justification='left')

try:
    while True:
        event, values = window.read()
        if event is None:
            break
        if event == '_PROCESS_' or event == '_TEST_':
            INPUT_DIR = values['_IN_IMG_']
            OUTPUT_DIR = values['_OUT_IMG_']
            BG_REMOVED_DIR = os.path.join(OUTPUT_DIR, '0_bg_removed')
            CROPPED_DIR = os.path.join(OUTPUT_DIR, '1_cropped')
            CROPPED_DIR_KAGE = os.path.join(OUTPUT_DIR, '1_cropped_kage')
            RESIZED_DIR = os.path.join(OUTPUT_DIR, '2_resized')
            RESIZED_DIR_KAGE = os.path.join(OUTPUT_DIR, '2_resized_kage')
            RENAMED_DIR = os.path.join(OUTPUT_DIR, 'output')
            RENAMED_DIR_KAGE = os.path.join(OUTPUT_DIR, 'output_helper')

            WIDTH = int(values['_NEW_WIDTH_'])
            HEIGHT = int(values['_NEW_HEIGHT_'])

            MTOP = int(values['_MARGIN_TOP_'])
            MRIGHT = int(values['_MARGIN_RIGHT_'])
            MBOTTOM = int(values['_MARGIN_BOTTOM_'])
            MLEFT = int(values['_MARGIN_LEFT_'])

            csvfile = values['_RENAME_CSV_']
            no_of_imgs = int(values['_IMG_ANGLES_'])


            if INPUT_DIR == '' or OUTPUT_DIR == '' or values['_NEW_WIDTH_'] == '' or values['_NEW_HEIGHT_'] == '' or values['_MARGIN_TOP_'] == '' or values['_MARGIN_RIGHT_'] == '' or values['_MARGIN_BOTTOM_'] == '' or values['_MARGIN_LEFT_'] == '' :
                print('please specify folders and input valid width & height')
            elif OUTPUT_DIR == INPUT_DIR:
                print('Output Folder cannot be same as the Input Folder')
            elif os.listdir(OUTPUT_DIR) :
                print('Output Folder must be Empty')
            elif csvfile == '':
                print('must speficy csv file with desired filename per line')
            elif no_of_imgs == '':
                print('must speficy no. of angles per image')
            elif event == '_TEST_':
                folder_init()
                touchitup("test")
                cropitup("test")
                resizeitup("test")
                renameitup("test")
                cleanitup()
            else:
                folder_init()
                touchitup()
                cropitup()
                resizeitup()
                renameitup()
                cleanitup()

except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened.  Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)