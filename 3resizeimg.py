import traceback
import os
from PIL import Image
import numpy as np
import PySimpleGUI as sg

image_exts = [ '.jpg', '.jpeg' ]

def resizeitup():
    desired_size = (WIDTH - PADDING_SIDES, HEIGHT)

    count = 0
    for _, _, files in os.walk(INPUT_DIR):
        file_count = len(files)
        for filename in files:
            count +=1
            file_path = os.path.join(INPUT_DIR, filename)
            file_name, file_ext = os.path.splitext(file_path)
            output_file_name = os.path.basename(file_name) + file_ext # save imagename (change ext if you want)
            # if the output file already exists, skip it
            if os.path.isfile(f'{OUTPUT_DIR}/{output_file_name}'):
                print('output file already exists, skipping...')
                continue

            if file_ext not in image_exts:
                print("Skipping " + filename + " (not a supported image file)")
                count -=1
                file_count -= 1
                continue

            else:
                i = Image.open(f'{INPUT_DIR}/{filename}')
                old_size = i.size
                ratio = min([float(desired_size[0])/old_size[0], float(desired_size[1])/old_size[1]])
                new_size = tuple([int(x*ratio) for x in old_size])
                im = i.resize(new_size, Image.ANTIALIAS)
                new_im = Image.new('RGB', size = (WIDTH, HEIGHT), color = (255, 255, 255)) #generate bg image (for jpg)
                # new_im = Image.new('RGBA', size = (WIDTH, HEIGHT), color = ("WHITE")) #generate bg image (for PNG)
                new_im.paste(im, ((WIDTH - new_size[0]) // 2, HEIGHT - new_size[1] - PADDING_BOTTOM))

                new_im.save(f'{OUTPUT_DIR}/{output_file_name}')

                print(f'{count}/{file_count} resizing {filename}... done.')


layout = [
    [sg.Text('Input folder with jpgs:')],
    [sg.Input(key='_IN_IMG_'), sg.FolderBrowse()],
    [sg.Text('Output folder:')],
    [sg.Input(key='_OUT_IMG_'), sg.FolderBrowse()],
    [sg.Text('')],
    [sg.Text('New Width (px):'), sg.InputText(1000, key='_NEW_WIDTH_', size=(5,1))],
    [sg.Text('New Height (px):'), sg.InputText(1000, key='_NEW_HEIGHT_', size=(5,1))],
    [sg.Text('Padding Sides (px):'), sg.InputText(40, key='_PADDING_SIDES_', size=(5,1))],
    [sg.Text('Padding Bottom (px):'), sg.InputText(280, key='_PADDING_BOTTOM_', size=(5,1))],
    [sg.Text('')],
    [sg.Button("Process", size=(10, 1), bind_return_key=True, key='_PROCESS_')],
    [sg.Output(size=(60, 10))],
]

window: object = sg.Window('Bulk Image Resize', layout, element_justification='left')

try:
    while True:
        event, values = window.read()
        if event is None:
            break
        if event == '_PROCESS_':
            INPUT_DIR = values['_IN_IMG_']
            OUTPUT_DIR = values['_OUT_IMG_']

            WIDTH = int(values['_NEW_WIDTH_'])
            HEIGHT = int(values['_NEW_HEIGHT_'])

            PADDING_SIDES = int(values['_PADDING_SIDES_'])
            PADDING_BOTTOM = int(values['_PADDING_BOTTOM_'])

            if INPUT_DIR == '' or OUTPUT_DIR == '' or PADDING_SIDES == '' or PADDING_BOTTOM == '' :
                print('please specify folders, must add values for paddings')
            elif OUTPUT_DIR == INPUT_DIR:
                print('Output Folder cannot be same as the Input Folder')
            # elif os.listdir(OUTPUT_DIR) :
            #     print('Output Folder must be Empty')
            else:
                resizeitup()

except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened.  Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)