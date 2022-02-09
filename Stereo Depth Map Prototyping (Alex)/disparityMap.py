#https://medium.com/@omar.ps16/stereo-3d-reconstruction-with-opencv-using-an-iphone-camera-part-iii-95460d3eddf0
#https://github.com/niconielsen32/ComputerVision/blob/master/depthMaps.py

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import os

left_image = cv.imread('l_k1.tif', cv.IMREAD_GRAYSCALE)
right_image = cv.imread('r_k1.tif', cv.IMREAD_GRAYSCALE)         

stereo = cv.StereoBM_create(numDisparities=0, blockSize=21)
# For each pixel algorithm will find the best disparity from 0
# Larger block size implies smoother, though less accurate disparity map
depth = stereo.compute(left_image, right_image)

print(depth)

cv.imshow("Left", left_image)
cv.imshow("right", right_image)

plt.imshow(depth)
plt.axis('off')
plt.show()

	