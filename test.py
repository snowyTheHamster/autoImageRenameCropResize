import os
import cv2
from PIL import Image
import numpy as np

#opencv opens image as a NumPy array in BGR
#Pillow opens image as a Pillow Object is RGB

# print(dir(cv2.imwrite))

# im = np.array(Image.open(f'{OLDIMG}').convert('L').resize((256, 256)))
# print(type(im))

# im = cv2.imread(f'{OLDIMG}')
# im_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

# Image.fromarray(im_rgb).save('testdir/test_pillow_conv.jpg')
# Image.fromarray(im).save('testdir/test_pillow_conv.jpg')
# cv2.imwrite('testdir/testing.jpg', im_rgb)
# cv2.imwrite('testdir/test_new.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 1])

OLDIMG = 'testdir/test.jpg'
BGIMG = 'testdir/bg.jpg'

src1 = cv2.imread(OLDIMG)
src2 = cv2.imread(BGIMG)

src1 = cv2.resize(src1, src2.shape[1::-1])

dst = cv2.addWeighted(src1, 1.0, src2, 0.1, 12)
cv2.imwrite('testdir/blended.jpg', dst)