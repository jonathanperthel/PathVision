import time
import socket
import cv2
import numpy as np
from realsense_depth import *
from IPython.display import clear_output

#sockets
host = "192.168.123.12"   #ip address of the robot's pi
port = 61626        #this number does not matter just needs to be the same across server and client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

#initialization
buffer = [0] * 40  #buffer moving average filter
dc = DepthCamera() #initialize intel realsense
position = 99
ret, depth_frame, color_frame, depth_frame2 = dc.get_frame()
rows, cols, _ = color_frame.shape
x_medium = int(cols/2)

#mainloop
while True:
    
    #stream from intel realsense
    ret, depth_frame, color_frame, depth_frame2 = dc.get_frame()

    #identifying red color
    hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)
    low_red = np.array([161, 155, 84])    #low end red color
    high_red = np.array([179, 255, 255])  #high end red color
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)

    #finding largest red object
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    #this follows the largest red object
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(color_frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
        x_medium = int((x + x + w)/2)
        break
    cv2.line(color_frame, (x_medium, 0), (x_medium, 480), (255,0,255), 2)
    
    #use moving average buffer to stabilize output distance
    dist1 = np.min(depth_frame[np.nonzero(depth_frame)])
    buffer[0] = dist1
    for i in range(len(buffer)):
        buffer[len(buffer)-1-i] = buffer[len(buffer)-2-i]
    dist1 = round(np.mean(dist1)/10)*10
    print(dist1)
    
    #shows frame
    cv2.imshow('depth_frame', depth_frame2)
    cv2.imshow('color_frame', color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
    
    #movement commands
    position = int(x_medium/8)
    print(position)
    
    if position < 10:
        position = 10
    elif position > 84:
        position = 84
    if dist1 < 500:
        position = 99
        print('stop')
    
    #send commands
    command = str(position)
    s.sendall(command.encode())

s.close
cv2.destroyAllWindows



