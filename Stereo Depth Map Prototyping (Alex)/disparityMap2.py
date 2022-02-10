#https://github.com/niconielsen32/ComputerVision/blob/master/stereoVisionCalibration/stereovision.py
#calibration checkerboards: https://markhedleyjones.com/projects/calibration-checkerboard-collection

#NEXT STEP:
#https://stackoverflow.com/questions/23039961/getting-real-depth-from-disparity-map
#https://learnopencv.com/depth-perception-using-stereo-camera-python-c/#from-disparity-map-to-depth-map
import numpy as np
import cv2


# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()


# Open both cameras
cap_right = cv2.VideoCapture(0, cv2.CAP_DSHOW)                    
cap_left =  cv2.VideoCapture(2, cv2.CAP_DSHOW)

#stereo param
stereo = cv2.StereoBM_create(32,29)

while(cap_right.isOpened() and cap_left.isOpened()):

    succes_right, frame_right = cap_right.read()
    succes_left, frame_left = cap_left.read()

    # Undistort and rectify images
    frame_right = cv2.remap(frame_right, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    frame_left = cv2.remap(frame_left, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    frame_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    frame_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)
    disparity = stereo.compute(frame_left, frame_right)

    #modify params for disparity
    disparity = disparity.astype(np.float32)
    disparity = (disparity/16.0 - 17)/17

    #map = disparity
    disparity = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)#C3)
    map = cv2.applyColorMap(disparity, cv2.COLORMAP_AUTUMN)
    #map = cv2.Canny(map, 30, 255)
    #map = cv2.erode(map, (2,2), iterations=1)
                     
    # Show the frames
    cv2.imshow("frame right", frame_right) 
    cv2.imshow("frame left", frame_left)
    cv2.imshow("right", map)


    # Hit "q" to close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release and destroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()