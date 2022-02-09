#https://github.com/niconielsen32/ComputerVision/blob/master/stereoVisionCalibration/calibration_images.py
#https://www.youtube.com/watch?v=yKypaVl6qQo
import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)

num = 0

while cap.isOpened():

    succes1, img = cap.read()
    succes2, img2 = cap2.read()

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k%256 == 32: # wait for 's' key to save and exit
        cv2.imwrite('frameL'+str(num)+'.png', img)
        cv2.imwrite('frameR'+str(num)+'.png', img2)
        print("images saved!")
        num += 1

    cv2.imshow('Img 1',img)
    cv2.imshow('Img 2',img2)

# Release and destroy all windows before termination
cap.release()
cap2.release()

cv2.destroyAllWindows()