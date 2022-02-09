#https://learnopencv.com/tag/cv2-stereobm/
#https://learnopencv.com/depth-perception-using-stereo-camera-python-c/#from-disparity-map-to-depth-map
#relevant post

import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)

# Check if the webcam is opened correctly
if not cap.isOpened() or not cap2.isOpened():
    raise IOError("Cannot open webcam")
stereo = cv2.StereoBM_create(numDisparities=0, blockSize=39)

while True:
    ret, frame = cap.read()
    ret, frame2 = cap2.read()

    left = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    right = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    disparity = stereo.compute(left, right)
    disparity = cv2.normalize(disparity, disparity, alpha=100, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    cv2.imshow('left', left)
    cv2.imshow('right', right)
    cv2.imshow('disparity', disparity)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cap2.release()
cv2.destroyAllWindows()