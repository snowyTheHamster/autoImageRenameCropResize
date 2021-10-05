import traceback
import os
import sys, shutil
import PySimpleGUI as sg
import csv


def renameitup():

    # create temp folder
    try:
        os.mkdir(TMP_DIR)
    except:
        print('directory already exists')

    # Copy & paste all files from input_dir to temp folder
    for _, _, files in os.walk(INPUT_DIR):
        for filename in files:
            file_path = os.path.join(INPUT_DIR, filename)
            temp_file_path = os.path.join(TMP_DIR, filename)
            shutil.copy2(file_path, temp_file_path)


    count = 0
    for _, _, files in os.walk(TMP_DIR):

        f = open(csvfile, encoding='utf-8')
        csv_f = csv.reader(f)

        file_count = len(files)
        for filename in files:
            count +=1
            file_path = os.path.join(TMP_DIR, filename)
            file_name, file_ext = os.path.splitext(file_path)

            for row in csv_f: # per each row in csv file
                for y in range(int(row[1])): # repeat below loop x number of times per csv row
                    y = y + 1

                    if y == 1:
                        new_file = f'SH_{row[0]}_XL{file_ext}' # create desired filename from csv
                    elif y > 1:
                        new_file = f'SH_{row[0]}_0{y-1}_XL{file_ext}' # create desired filename from csv


                    the_files = sorted(os.listdir(TMP_DIR)) # gets list of files in a directory (add sorted or it won't work on some workstations)
                    file_old_path = os.path.join(TMP_DIR, the_files[0]) # set fullpath of first file in directory
                    file_new_path = os.path.join(OUTPUT_DIR, new_file) # set fullpath of file in target directory
                    shutil.move(file_old_path, file_new_path) # moves renamed file to target directory

                    print(f'{count}/{file_count} rename {filename}, move to {file_new_path}.. done.')

    # delete temp folder
    try:
        shutil.rmtree(TMP_DIR, ignore_errors=True)
    except:
        print(f'failed to delete temp folder')


layout = [
    [sg.Text('Input folder:')],
    [sg.Input(key='_IN_FILE_'), sg.FolderBrowse()],
    [sg.Text('Output folder:')],
    [sg.Input(key='_OUT_FILE_'), sg.FolderBrowse()],
    [sg.Text('')],
    [sg.Text('csv with 1 filename/line:'), sg.Input(key='_RENAME_CSV_'), sg.FileBrowse()],
    [sg.Button("Process", size=(10, 1), bind_return_key=True, key='_PROCESS_')],
    [sg.Output(size=(60, 10))],
]

window: object = sg.Window('Bulk File Rename', layout, element_justification='left')

try:
    while True:
        event, values = window.read()
        if event is None:
            break
        if event == '_PROCESS_':
            INPUT_DIR = values['_IN_FILE_']
            OUTPUT_DIR = values['_OUT_FILE_']
            TMP_DIR = os.path.join(OUTPUT_DIR, 'temp_dir')

            csvfile = values['_RENAME_CSV_']

            if INPUT_DIR == '' or OUTPUT_DIR == '':
                print('please specify folders')
            elif OUTPUT_DIR == INPUT_DIR:
                print('Output Folder cannot be same as the Input Folder')
            elif os.listdir(OUTPUT_DIR) :
                print('Output Folder must be Empty')
            elif csvfile == '':
                print('must speficy csv file with desired filename per line')
            else:
                renameitup()

except Exception as e:
    tb = traceback.format_exc()
    sg.Print(f'An error happened.  Here is the info:', e, tb)
    sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)