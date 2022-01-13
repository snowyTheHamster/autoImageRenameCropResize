# autoImageRenameCropResize

Automate image processing using python and OpenCV.

These scripts will in bulk:

1. Detects largest object in the images and removes the background.
1. Detects the edges of object and crops the images.
1. Resizes images to desired size.
1. Renames images by supplying a csv with a list of names.

Run each of these scripts to launch a gui app.

You can also run the .ipynb versions on Google Colabs.

To run on your workstation, you will need to install python from [https://www.python.org/](https://www.python.org/)

When prompted, make sure to set python to PATH and install PIP.

### Create a Project Directory
```
mkdir myprojectname
cd myprojectname
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
python -m pip install --upgrade pip
pip install -r requirements.txts
```

## Running 1removebg_upgraded.py (upgraded)

1. prepare folder with images you want to process (input folder).
1. create a folder to output the results.
1. Copy the files in the input folder to the output folder.
1. You can adjust the threshold, set the new background color by adjusting the rgb sliders.
2. Click Process and hit Enter.
3. Once your happy with a result, remove it from the output folder and repeat.

```
python 1removebg_upgraded.py
```

**NOTE:** Detecting white objects against a white background is difficult.

To maximize the success rate, try to **blowing out your white background** during the photo shoot.

Keep your object's edges as distinct from the background as possible.

**Installing the GUI app**

to install this script as a gui app, run the following commands:

```
pyinstaller --onefile 1removebg_upgraded.py
```

The executable app will be saved in the dist folder for your operating system.

---

**NOTE 2:** You can change the parameters if the defaults don't yield good results.

## Running 2cropimg.py

1. prepare folder with images (backgrounds removed)
1. prepare optional folder with images (without the backgrounds removed)
1. create a folder to output the results

```
python 2cropimg.py
```

This script will detect the edges of the object in the images and crop around the edges.

You can add extra paddings by changing the settings.

## Running 3resizeimg.py

1. prepare folder with images
1. create a folder to output the results
1. set desired width & height of new images
1. Padding Sides will distribute paddings horizontally (e.g. 40px means 20px on left & right)
1. Padding Bottom adds padding to bottom of the images.

```
python 3resizeimg.py
```

This script essentially creates a new image (white background) in the desired size and pastes the original image into it.


## Running 4renamefiles.py

1. prepare folder with images
1. create a folder to output the results
1. prepare csv file with one filename per line (no headers, first column only)
1. Input **no. per file**. If you have several angles of same product photo (for example 3 angles per product, type in 3).

This script does not alter the **input folder** so you can experiment with it.

```
python 4renamefiles.py
```

**Note**

- The number of images in input folder must match the rows of filenames in the csv file.
- If you have multiple angles of product images, they all they to be the same (e.g. if product shots have 3 angles, they all have to have 3 angles).

**Scenario 1**

60 images, 1 angle(s) per image, set **no. per file** to **1** -> csvfile will contain 60 rows of filename.

output will be: row1name_1.jpg, row2name_1.jpg, row3name_1.jpg, row4name_1.jpg etc..

**Scenario 1**

60 images, 2 angle(s) per image, set **no. per file** to **2** -> csvfile will contain 30 rows of filename.

output will be: row1name_1.jpg, row1name_2.jpg, row2name_1.jpg, row2name_2.jpg etc..

**Note 2**

These scripts won't affect the original images but you should still make back ups.