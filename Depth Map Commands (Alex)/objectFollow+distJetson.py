#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import socket
import time
import socket
import cv2
import numpy as np
from realsense_depth import *
from IPython.display import clear_output

#sockets:---------------------------------------------------------------------------------------------------------
host = "192.168.123.12"   #ip address of the robot's pi
port = 61626        #this number does not matter just needs to be the same across server and client

# set up socket connection, server needs to be started first**
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
#-----------------------------------------------------------------------------------------------------------------

buffer = [0] * 40  #buffer moving average filter
dc = DepthCamera() #initialize intel realsense
position = 49       #degrees

#set frames (if no red object detected)
ret, depth_frame, color_frame, depth_frame2 = dc.get_frame()
rows, cols, _ = color_frame.shape
x_medium = int(cols/2)
y_medium = int(rows/2)
center = int(cols/2)

while True:
    
    #stream from intel realsense
    ret, depth_frame, color_frame, depth_frame2 = dc.get_frame()
    kernel = np.ones((2,2), np.uint8)
    #depth_frame2 = cv2.dilate(depth_frame2, kernel, iterations=25)
    depth_frame = cv2.dilate(depth_frame, kernel, iterations=20)
    depth_frame = cv2.blur(depth_frame,(2,2)) 
    depth_frameDISP = cv2.normalize(depth_frame, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    #identifying red color
    hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)
    low_red = np.array([161, 155, 84]) #low end red color
    high_red = np.array([179, 255, 255]) #high end red color
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)

    #finding largest red object
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    #this follows the largest red object
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        cv2.rectangle(color_frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
        x_medium = int((x + x + w)/2)
        y_medium = int((y + y + h)/2)
        break

    #cv2.line(color_frame, (x_medium, 0), (x_medium, 480), (255,0,255), 2)
    point1 = (x_medium,y_medium)
    cv2.circle(depth_frame, point1, 4, (255, 192, 203))
    cv2.circle(depth_frameDISP, point1, 4, (255, 192, 203))
    
    #use moving average buffer to stabilize output distance
    dist1 = depth_frame[y_medium, x_medium]
    buffer[0] = dist1
    for i in range(len(buffer)):
        buffer[len(buffer)-1-i] = buffer[len(buffer)-2-i]
    dist1 = round(np.mean(dist1)/100)*100
    
    clear_output(wait=True)
    print(dist1)
    
    #shows frame
    #cv2.imshow('red_mask', red_mask)
    cv2.imshow('depth_frame', depth_frameDISP)
    cv2.imshow('color_frame', color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

    print(x_medium)
    
    #movement commands
    position = int(x_medium/8)
    print(position)
    if position < 10:
        position = 10
    elif postion > 84:
        position = 84
    if dist1 < 300:
        position = 99
    
    #print(position)
    command = str(position)
    s.sendall(command.encode())

s.close
cv2.destroyAllWindows


# In[ ]:




