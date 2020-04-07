# autoImageRenameCropResize

Some python scripts that use OpenCV's features automate some photo retouching.

These scripts will:

+ Detects the edges of an object in an image
+ Replaces background with Pure White
+ Crops the images
+ Resizes the images
+ Renames the images

### Create a Project Directory
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

## Setting up

+ Ensure folder names and settings are correct in each file

Ensure you have these folders and files:

+ 0_input_images (add all your images here)
+ 1_bg_removed   (script that removes bg without clipping highlights but may result in fuzzy edges)
+ 1_bg_removed_b (stript that removes bg with clean edges but prone to clipping highlights)
+ 2_cropped      (crops images from 1_bg_removed)
+ 2_cropped_b    (crops images from 1_bg_removed_b but uses same dimensions as 1_bg_removed)
+ 3_resized800   (resized images in 2_cropped)
+ 3_resized800_b (resized images in 2_cropped_b)
+ 4_renamed      (renames images in 3_resized)
+ 4_renamed_b    (renames images in 3_resized_b)
+ backgrounds
+ list.csv (input your list of filenames here for **rename** scripts to work)

## Running the script

**NOTE:** Detecting white objects against a white background is difficult.

To maximize the success rate, try to **clip out your white background** as bright as possible whilst 

keeping your object's edges as distinct from the background as possible.

---

**NOTE 2:** You may need to play with the parameters in the **removebgA.py** & **removebgB.py** scripts.

Parameters to change in removebgA.py:

+ bilateralFilter
+ Canny
+ getStructuringElement

Parameters to change in removebgB.py:

+ MIN_VAL
+ bilateralFilter
+ getStructuringElement

Place your images in the **inputimages** folder and run scripts in the following order:

```
python removebgA.py
python removebgB.py
python cropA.py
python cropB.py
python resizeA.py
python resizeB.py
python renameA.py
python renameB.py
```

or run all the scripts at once:

```
python 0-run.py
```

Each script will perform a different task.

This allows you to make manual adjustments in between.

The quality of the output will depend on:

+ Quality of the image
+ The background in the image (the brighter and cleaner, the better)
+ Difference between the object and the background (products with fuzzy edges and bright edges are difficult) 
+ Parameter settings in each script.

**NOTE:**

The **removebgB.py** script produces the best quality results but only when the edges are distinct from background.

It is very prone to highlights being clipped.

That is why I included **removebg.py** which is configured to prevent highlights from clipping, but has fuzzy edges.

By running both scripts, you will end up with images that are cropped and resized the same; this can allow you to 

stack the images in a photo-editor for easier editing later.


## Resizing Images

The resize scripts will output images to 800x800.

This is hard-coded at the moment.

To change this, edit the resize scripts and also provide a pure-white bg img in the **backgrounds** folder.

## Renaming Images

You need to provide a list of filenames in the **list.csv** file.

You also need to edit the logic in the rename scripts.

The method used for renaming is basic python string manipulation.