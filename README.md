# autoImageRenameCropResize

A Python script that detects the edges of an object and replaces the background with pure white.

## Setting up


### Create a Project Directory**
```
mkdir myprojname
cd myprojname
```

### Clone the Repo
```
git clone https://github.com/snowyTheHamster/autoImageRenameCropResize.git .
```

### Create a virtual Environment
```
python -m venv .venv
```

**Active the virtual Env in Mac and Linux:**
```
. .venv/bin/activate

```

**Active the virtual Env in Windows:**
```
. .venv/script/activate

```

### Install the modules from the provided req file
```
pip install -r requirements.txt
```

## Running the script

+ Ensure folder names and settings are correct in each file

Place your images in the **inputimages** folder and run scripts in the following order:

```
python 1-removebg.py
python 1b-removebg.py
python 2-crop.py
python 3-resize.py
python 4-rename.py
```

Each script will perform a different task.

This allows you to make adjustments in between in case the results were not perfect.

The quality of the output will depend on:

+ Quality of the image
+ Exposure of the background in the image (the brighter the better)
+ Difference between the object in the image and the background (white products are more difficult). 
+ Parameter settings in each script.

### 1-removebg.py

This script detects the edges of an object whilst trying to prevent white clipping.

There may be some fuzziness around object which will be removed in the next script.

You will need to adjust the **MIN_VAL** **MAX_VAL** settings.

The resulting images will generated in a different folder for you to finetune.

An image will not be processed if it already exists in the output folder; so you can re-run the script accordingly.

### 1b-removebg.py

This script tries to remove the fuzziness around the object made in the previous script.

The resulting images will generated in a different folder for you to finetune.

An image will not be processed if it already exists in the output folder; so you can re-run the script accordingly.

### 2-crop.py

This script detects the edges of the images again and crops the image.

This step makes it easier to resize the image for the next script.

This script will work on the output of the previous step.

An image will not be processed if it already exists in the output folder; so you can re-run the script accordingly.

### 3-resize.py

This script resizes the images from the previous cropped images.

This script will work on the output of the previous step.

An image will not be processed if it already exists in the output folder; so you can re-run the script accordingly.

### 4-rename.py

This script renames all the images in a folder according to the settings in the script.

You also need to provide a csv file for this script to work.

This script renames **moves** images from previous folder to the next output folder.

Input Folder must ONLY contain images.