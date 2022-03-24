
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

cap = cv2.VideoCapture(0) #Capture first frame
position = 49 #degrees

#sets line value if no red object detected
_, frame = cap.read()
rows, cols, _ = frame.shape
x_medium = int(cols/2)
center = int(cols/2)

while True:
    #get input here
    #for now will simulate as a while look that prints 1 out ten times

    #data = [0,1,2,3,4,5,6,7,8,9]
    #reads in the frame
    _, frame = cap.read()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #identifying red color
    low_red = np.array([161, 155, 84]) #low end red color
    high_red = np.array([179, 255, 255]) #high end red color
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)

    #finding largest red object
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    #this follows the largest red object
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        #cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
        x_medium = int((x + x + w)/2)
        break

    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0,255,0), 2)

    #shows frame
    #cv2.imshow("Frame", frame)
    #cv2.imshow("mask", red_mask)

    #key = cv2.waitKey(1)

    #if key == 27:
     #   break

    #move robot
    position = int(x_medium/8)
    
    #print(position)

    s.sendall(bytes(position))
    data = s.recv(1024)
    print(data)
    time.sleep(2)


'''    for i in position:
        #send string, notice string needs to be in bytes form, this is the simplest way to do this
        #can probably find a better way to convert, especially if we want to use a preset variable
        s.sendall(b"1")

        #collect and print data recieved
        data = s.recv(1024)
        print(data)

        # arbitrary wait time for ease of testing can delete later if needed
        time.sleep(2)
    break
'''

#close connection
s.close()
#when the program is stopped, this closes all windows
cap.release()
cv2.destroyAllWindows