import os


for i in range(160):
    locaimgsdir = "inputimages"
    locainputdir = os.path.join("." , locaimgsdir)

    imgs = sorted(os.listdir(locainputdir)) # gets list of images in a directory
    imgoldpath = os.path.join(locainputdir, imgs[0]) # set fullpath of first image in directory

    print (f'the filename is: {imgoldpath} \n')