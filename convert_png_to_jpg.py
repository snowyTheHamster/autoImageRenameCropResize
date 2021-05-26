import traceback
import os
from PIL import Image
import PySimpleGUI as sg

image_exts = [ '.png' ]

def convert():

    count = 0
    for _, _, files in os.walk(INPUT_DIR):
        file_count = len(files)
        for filename in files:
            count +=1
            file_path = os.path.join(INPUT_DIR, filename)
            file_name, file_ext = os.path.splitext(file_path)
            output_file_name = os.path.basename(file_name) + '.jpg'

            if file_ext not in image_exts:
                print("Skipping " + filename + " (not a supported image file)")
                count -=1
                file_count -= 1
                continue

            else:
                i = Image.open(f'{INPUT_DIR}/{filename}')
                new_image = Image.new("RGBA", i.size, "WHITE") # Create a white rgba background
                new_image.paste(i, (0, 0), i)
                output_final = os.path.join(OUTPUT_DIR, output_file_name)
                new_image.convert('RGB').save(output_final, "JPEG")

                print(f'{count}/{file_count} converting {filename} to JPG.. DONE.')




layout = [
    [sg.Text('Input folder with png files:')],
    [sg.Input(key='_IN_IMG_'), sg.FolderBrowse()],
    [sg.Text('Output folder:')],
    [sg.Input(key='_OUT_IMG_'), sg.FolderBrowse()],
    [sg.Text('')],
    [sg.Button("Process", size=(10, 1), bind_return_key=True, key='_PROCESS_')],
    [sg.Output(size=(60, 10))],
]

window: object = sg.Window('Convert PNG to JPG', layout, element_justification='left')

try:
    while True:
        event, values = window.read()
        if event is None:
            break
        if event == '_PROCESS_':
            INPUT_DIR = values['_IN_IMG_']
            OUTPUT_DIR = values['_OUT_IMG_']

            if INPUT_DIR == '' or OUTPUT_DIR == '':
                print('please specify folders, must add values for paddings')
            elif OUTPUT_DIR == INPUT_DIR:
                print('Output Folder cannot be same as the Input Folder')
            elif os.listdir(OUTPUT_DIR) :
                print('Output Folder must be Empty')
            else:
                convert()

except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened.  Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)