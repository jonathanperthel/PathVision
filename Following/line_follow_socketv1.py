
import socket
import time
import cv2
import numpy as np

host = "192.168.123.12"   #ip address of the robot's pi
port = 61626        #this number does not matter just needs to be the same across server and client

# set up socket connection, server needs to be started first**
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# send handshake to the server
s.sendall(b'socket connected!')
data = s.recv(1024)
#print out data recieved
print(data)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

angle = 0

while True:
    # Capture the frames
    ret, frame = cap.read()
    cv2.imshow('frame',frame)

    # Crop the image
    #crop_img = frame[60:120, 0:160]

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('grayscale',gray)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray,(5,5),0)
    #cv2.imshow('blurred',blur)

    # Color thresholding
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    #cv2.imshow('with_threshold',thresh)

    # Try adjusting the prameters on the above filters and transformations to see what happens!

    # Find the contours of the frame
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)


    # Find the biggest contour (if detected)
    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        try:
            M = cv2.moments(c)
            # Identify line from the countours
            # Here cx, cy indicates the center of the line (which will be the biggest contour on the image)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #print(cx, cy)

            cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)
            cv2.drawContours(frame, contours, -1, (0,255,0), 1)

            angle = int(cx/8)
            if angle < 10:
                angle = 10
        except:
            #print("I don't see the line")
            angle = 99

    #Display the resulting frame
    cv2.imshow('frame',frame)

    print(angle)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    s.sendall(bytes(angle))
    data = s.recv(1024)
    print(data)
    time.sleep(2)



#close connection
s.close()
#when the program is stopped, this closes all windows
cap.release()
cv2.destroyAllWindows