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

+ Ensure folder names and settings are correct in each file.

Explanation of each folder and file:

+ 0_input_images (add all your images here)
+ 1_bg_removed   (outputs bg-removed imgs using threshold)
+ 1_bg_removed_b (outputs bg-removed imgs using canny algorithm)
+ 2_cropped      (cropped imgs saved here)
+ 2_cropped_b    (cropped imgs saved here)
+ 3_resized800   (resized imgs saved here)
+ 3_resized800_b (resized imgs saved here)
+ 4_renamed      (renamed imgs saved here)
+ 4_renamed_b    (renamed imgs saved here)
+ backgrounds
+ list.csv (list your filenames here for **rename** scripts to work)

## Running the script

**NOTE:** Detecting white objects against a white background is difficult.

To maximize the success rate, try to **blowing out your white background** during the photo shoot.

Keep your object's edges as distinct from the background as possible.

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

Each script will perform one task.

The results from each task is saved in a unique folder.

This allows you to make manual adjustments in between.

The quality of the output will depend on:

**NOTE:**

The **removebgB.py** script produces the best quality results but only when the edges are distinct from background.

It produces poor results for light colored objects.

That's why I included **removebgA.py** which is configured to minimize highlights from clipping, but results in fuzzy edges.

Run both scripts; you'll end up with 2 sets of results with equal crop/size.

Stack these images in a photo-editor for finetuning.


## Resizing Images

The resize scripts will output images to 800x800.

This is hard-coded at the moment.

To change this, edit the resize scripts and also provide a pure-white bg img in the **backgrounds** folder.


## Renaming Images

You need to provide a list of filenames in the **list.csv** file.

You also need to edit the logic in the rename scripts.

The method used for renaming is basic python string manipulation.