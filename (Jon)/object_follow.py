#from turtle import position
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#cap.set(3, 480)
#cap.set(4, 320)
position = 90 #degrees

#sets line value if no red object detected
_, frame = cap.read()
rows, cols, _ = frame.shape
x_medium = int(cols/2)
center = int(cols/2)

while True:

    #reads in the frame
    _, frame = cap.read()

    #read for intel?
    ret, frame, depth_frame = rs.get_frame_stream()


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
    cv2.imshow("Frame", frame)
    cv2.imshow("mask", red_mask)

    key = cv2.waitKey(1)

    if key == 27:
        break

    #move robot
    if x_medium < center - 30:
        position += 1
    elif x_medium > center + 30:
        position -= 1
    
    print(position)

#when the program is stopped, this closes all windows
cap.release()
cv2.destroyAllWindows