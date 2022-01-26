import numpy as np
import cv2
import torch


image = cv2.imread('test.jpeg',0)
radius = 100
center = (150,150)
color = (255,255,0)
thickness = 15

image = cv2.circle(image, center, radius, color, thickness)
image = cv2.resize(image, (200,200))
cv2.imshow('circle', image)
cv2.waitKey(0)
cv2.destroyAllWindows()