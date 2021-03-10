# autoImageRenameCropResize

Automate image processing using python and OpenCV

These scripts will in bulk:

1. Detects largest object in the images and removes the background.
1. Detects the edges of object and crops the images.
1. Resizes images to desired size.
1. Renames images by supplying a csv with a list of names.

Run each of these scripts to launch a gui app.

You can also use the .ipynb notebooks on Google Colabs.


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
pip install -r requirements.txt
```

## Running 1removeby.py

1. prepare folder with images you want to process
1. create a folder to output the results
1. You can set the new background color by adjusting the rgb sliders.

`python 1removebg.py`

**NOTE:** Detecting white objects against a white background is difficult.

To maximize the success rate, try to **blowing out your white background** during the photo shoot.

Keep your object's edges as distinct from the background as possible.

---

**NOTE 2:** You can change the parameters if the defaults don't yield good results.

## Running 2cropimg.py

1. prepare folder with images (backgrounds removed)
1. prepare optional folder with images (without the backgrounds removed)
1. create a folder to output the results

`python 2cropimg.py`


This script will detect the edges of the object in the images and crop around the edges.

You can add extra paddings by changing the settings.

## Running 3resizeimg.py

1. prepare folder with images
1. create a folder to output the results
1. set desired width & height of new images
1. Padding Sides will distribute paddings horizontally (e.g. 40px means 20px on left & right)
1. Padding Bottom adds padding to bottom of the images.

`python 3resizeimg.py`

This script essentially creates a new image (white background) in the desired size and pastes the original image into it.


## Running 4renamefiles.py

1. prepare folder with images
1. create a folder to output the results
1. prepare csv file with one filename per line (no headers, first column only)
1. Input **no. per file**. If you have several angles of same product photo (for example 3 angles per product, type in 3).

This script does not alter the **input folder** so you can experiment with it.

`python 4renamefiles.py`

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

Rename function will work on files with any filetype, not just jpgs.

## Samples

You can test the script with the sample images included in the **sample_images** folder.

These images are significantly downsized so the results are poor, but should give you an idea of what type of photos work.