import cv2
from realsense_camera import *
 
#Load Realsense camera
rs = RealsenseCamera()

while True:
    ret, bgr_frame, depth_frame = rs.get_frame_stream()

    cv2.imshow("Bgr frame", bgr_frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

