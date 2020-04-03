# autoImageRenameCropResize

A script that detects the edges of an object and replaces the background with pure white.

## Setting up


### Create a Project Directory**
```
mkdir mydirrrrrr
cd mydirrrrrr
```

### Clone the Repo
```
git clone https://github.com/snowyTheHamster/autoImageRenameCropResize.git .
```

### Create and activate a virtual Environment
```
python -m venv .venv
```

**Mac and Linux:**
```
. .venv/bin/activate

```

**Windows:**
```
. .venv/script/activate

```

### Install the modules
```
pip install -r requirements.txt
```

## Running the script

Create the following folders in the project folder if they don't yet exist:

```
mkdir renamed
```

### Running the background replacement

Place your images in the **renamed** folder and run the script:

```
python crop.py
```

The background should be replaced with pure white BG and the new images should be saved in **resized800** folder.

All images will also be cropped and resized to 800x800 pixels.

These settings can be change in the **crop.py** file.

**Note:**

The quality of the output will depend on the original image and the parameters set in the **crop.py** file.

## Extra - rename images

You can bulk rename images with the **rename.py** script.

Create the input folder:

```
mkdir inputimages
```
 
place all images in the **inputimages** folder.

Prepare a **list.csv** with the list of items for the filenames.

Modify **rename.py** to set the rules for renaming the images.

run the rename script:

```
python rename.py
```

All the images in the **inputimages** folder should be renamed and moved to the **renamed** folder according to the logic written in the **rename.py** file.