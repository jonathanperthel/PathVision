import numpy as np
import cv2

class lineDetect:
    def coordinates ():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        
        #we are going to need to create the video in the main file
        #next we will call the class to return coordinates
        #then these coordinates will be used to determine if we are going left/right
        #then we will use math to determine the angle at which the robot must turn