import numpy as np
import matplotlib.pyplot as plt
import cv2

#enter image or camera stream here
img = cv2.imread('sample_picture.jpg')
img = img[0:, 200:780]

kernel = np.ones((5,5), np.uint8)
img = cv2.dilate(img, kernel, iterations=20)
vert, horiz, channels = np.shape(img)

#filter for red
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([107, 190, 240])
upper = np.array([120, 255, 255])
mask = cv2.inRange(hsv, lower, upper)

#applys the mask
frame = cv2.bitwise_and(img, img, mask=mask)

#find contours of object
cont, hierarch = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if len(cont) != 0:
    for mask_contour in cont:
        if cv2.contourArea(mask_contour) > 100:
            x, y, w, h = cv2.boundingRect(mask_contour)
            x2 = x + w
            y2 = y + h
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 3) #drawing rectangle

#reset img with lines
imgL = frame

#divide image into zones:
divLeft = round(horiz / 3)
divRight = 2*divLeft

#left line
topLeft = (divLeft, 0)
botLeft = (divLeft, vert)

#right line
topRight = (divRight, 0)
botRight = (divRight, vert)

color = (0, 255, 0)
thickness = 3
imgL = cv2.line(imgL, topLeft, botLeft, color, thickness)
imgL = cv2.line(imgL, topRight, botRight, color, thickness)

#area of image in left (image can be in left, left+center, or left+center+right)
if (x < divLeft):
    #left only
    leftLen = divLeft-x
    leftArea = leftLen*h
    print('left: ' +str(leftArea))
    
    #left+center (LIKELY BUG HERE IF case: left+center+right)
    if (x2 < divRight):
        cenLen = x2-divLeft
        cenArea = cenLen*h
        print('center: '+str(cenArea))
        
    #left+center+right
    if (x2 > divRight):
        rightLen = x2-divRight
        rightArea = rightLen*h
        print(rightArea)
        print('right: '+str(rightArea))

#area of image in right (image can be in right only)
elif (x > divRight):
    rightLen = w
    rightArea = w*h
    print('right: '+str(rightArea))
    
#area of image in center (image can be in center, center+right)
else:
    #center only
    cenLen = divRight-x
    cenArea = cenLen*h
    print('center: '+str(cenArea))

    #center+right
    if (x2 > divRight):
        rightLen = x2-divRight
        rightArea = rightLen*h
        print('right: '+str(rightArea))

plt.imshow(imgL)
plt.show()