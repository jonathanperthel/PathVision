import cv2
import pyrealsense2
from realsense_depth import *

point1 = (110, 240)
point2 = (330, 240)
point3 = (550, 240)

def show_distance(event, x, y, args, params):
    global point
    point = (x, y)

# Initialize Camera Intel Realsense
dc = DepthCamera()

# Create mouse event
#cv2.namedWindow("Color frame")
#cv2.setMouseCallback("Color frame", show_distance)

while True:
    ret, depth_frame, color_frame, depth_frame2 = dc.get_frame()
    kernel = np.ones((2,2), np.uint8)
    depth_frame2 = cv2.dilate(depth_frame2, kernel, iterations=25)
    depth_frame = cv2.dilate(depth_frame, kernel, iterations=20)
    depth_frame = cv2.blur(depth_frame,(2,2)) 
    depth_frameDISP = cv2.normalize(depth_frame, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    # Show distance for a specific point
    cv2.circle(color_frame, point1, 4, (0, 0, 255))
    cv2.circle(color_frame, point2, 4, (0, 0, 255))
    cv2.circle(color_frame, point3, 4, (0, 0, 255))
    dist1 = depth_frame[point1[1], point1[0]]
    dist2 = depth_frame[point2[1], point2[0]]
    dist3 = depth_frame[point3[1], point3[0]]
    
    #logic:
    if dist1 != 0 and dist2 != 0 and dist3 != 0:
        if dist1 > 500 and dist2 > 500 and dist3 > 500:
            print('\rforward',end='')
        
        #object in center, go left or right
        elif dist2 < dist1 and dist2 < dist3:
            if dist1 < dist3:
                print('\rright',end='')
            if dist3 < dist1:
                print('\rleft',end='')
        #object on left, go right
        elif dist1 < dist2 or dist1 < dist3:
            print('\rright',end='')
        #object on right go left
        elif dist3 < dist2 or dist3 < dist1:
            print('\rleft',end='')
    else:
        continue
    

    cv2.putText(color_frame, "{}mm".format(dist1), (point1[0], point1[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    cv2.putText(color_frame, "{}mm".format(dist2), (point2[0], point2[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    cv2.putText(color_frame, "{}mm".format(dist3), (point3[0], point3[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    
    cv2.imshow("depth frame2", depth_frame2)
    cv2.imshow("depth frame", depth_frameDISP)
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break