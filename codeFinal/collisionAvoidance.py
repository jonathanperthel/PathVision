#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import socket
import pyrealsense2 as rs
from realsense_depth import *

#sockets
host = "192.168.123.12"   #ip address of the robot's pi
port = 61626        #this number does not matter just needs to be the same across server and client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

#distance measurement points
point1 = (110, 240)
point2 = (330, 240)
point3 = (550, 240)

#initialize Camera Intel Realsense
dc = DepthCamera()

#movement command (stop by default)
cmd = 99

#define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('dotcam.avi', fourcc, 20.0, (640, 480))

while True:
    #image processing
    ret, depth_frame, color_frame, depth_frame2 = dc.get_frame()
    kernel = np.ones((2,2), np.uint8)
    depth_frame = cv2.dilate(depth_frame, kernel, iterations=20)
    depth_frame = cv2.blur(depth_frame,(2,2))

    #show distance for a specific point
    cv2.circle(color_frame, point1, 4, (0, 0, 255))
    cv2.circle(color_frame, point2, 4, (0, 0, 255))
    cv2.circle(color_frame, point3, 4, (0, 0, 255))
    dist1 = depth_frame[point1[1], point1[0]]
    dist2 = depth_frame[point2[1], point2[0]]
    dist3 = depth_frame[point3[1], point3[0]]
    
    #movement commands:
    if dist1 != 0 and dist2 != 0 and dist3 != 0:
        if dist1 > 500 and dist2 > 500 and dist3 > 500:
            print('no obstacle - move forward')
            cmd = 42
            
        #object in center, go left or right
        elif dist2 < dist1 and dist2 < dist3:
            if dist1 < dist3:
                print('obstacle center - move right')
                cmd = 20
            if dist3 < dist1:
                print('obstacle center - move left')
                cmd = 70
                
        #object on left, go right
        elif dist1 < dist2 or dist1 < dist3:
            print('obstacle left - move right')
            cmd = 20
            
        #object on right go left
        elif dist3 < dist2 or dist3 < dist1:
            print('obstacle right - move left')
    else:
        continue
    
    cv2.putText(color_frame, "{}mm".format(dist1), (point1[0], point1[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    cv2.putText(color_frame, "{}mm".format(dist2), (point2[0], point2[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    cv2.putText(color_frame, "{}mm".format(dist3), (point3[0], point3[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    
    cv2.imshow("depth frame2", depth_frame2)
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
        
    #video output
    out.write(color_frame) 
        
    #send commands
    command = str(cmd)
    s.sendall(command.encode())
    
s.close
cv2.destroyAllWindows


# In[ ]:




