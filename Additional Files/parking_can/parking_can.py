#******************************Autonomous parking************************************/
#------------------------------Line following algorithm------------------------------/
#------------------------------coded by Aravind AK-----------------------------------/
#******************supported by Rahul_R Jaswanth_I ID_Samueal Gautam_Raj*************/
# this is line fololwing code which is coded for Nvidia jetson TX2 on board camera
# the arduino should be connected via can sheild while executing this code 
# code can be configured for usb camera 
# should be optimised based on harware requirements 
# Most of dependencies comes with python3 on jetpack4.3
# if any dependencies is missing try adding the path or install it using 'pip' command 
#------------------------can communication is used------------------------------------/

# import required funtions 
import cv2 as cv
import utlis #make sure the utlis file is placed in same folder
import numpy as np
import time
from time import gmtime, strftime, sleep
import logging
import math


#enabling can communication
import os
os.system('sudo modprobe can')
os.system('sudo modprobe can_raw')
os.system('sudo modprobe mttcan')
os.system('sudo modprobe can_dev')
os.system('sudo ip link set can0 type can bitrate 500000')
os.system('sudo ip link set up can0')

#defining GStreamer Pipeline for Nvidia on board camera
def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

if __name__=='__main__':

    # capture the video stream data
    capture = cv.VideoCapture(gstreamer_pipeline(flip_method=0, framerate=60), cv.CAP_GSTREAMER)

    if not capture.isOpened:
        print('Unable to open: Camera interface')
        exit(0)
    print('Started')
    # commencing subtraction
    while True:
        try:
            # fetching each frame
            flag, frame = capture.read()

            if frame is None:
                break
            # Display camera input
            image = frame
            #define the processing reagion
            crop_img = frame[450:700, 450:780]
            
            # convert to grayscale, gaussian blur, and threshold
            gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray,(5,5),0)
            ret,th = cv.threshold(blur,60,255,cv.THRESH_BINARY_INV)
            edged = cv.Canny(blur, 85, 85)
            
            # Erode to eliminate noise, Dilate to restore eroded parts of image
            mask1 = cv.erode(th, None, iterations=2)
            mask = cv.dilate(mask1, None, iterations=2)

            # Find all contours in frame
            contours, hierarchy = cv.findContours(th.copy(),1,cv.CHAIN_APPROX_NONE)
	        # Find x-axis centroid of largest contour and cut power to appropriate motor
	        # to recenter camera on centroid. 
            if len(contours) > 0:
                    c = max(contours, key=cv.contourArea)
                    M = cv.moments(c)
                    
                    if M["m00"] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        print(cx,"value")

                        if cx >= 115 and cx <=190:
                            os.system('cansend can0 666#02')
                            #print(cx,"Straight")
                            
                        elif cx < 110:
                            os.system('cansend can0 666#01')
                            #print(cx,"left")
                        elif cx > 190:
                            os.system('cansend can0 666#03')
                            #print(cx,"Right")
                    else:
                        #print(cx,"value")
                        os.system('cansend can0 666#04')

            else:
                 print ("I don't see the line")
                 os.system('cansend can0 666#04')
            imgStacked = utlis.stackImages(0.7, ([crop_img,blur,th],
                                         [gray,edged,mask] ))

            cv.imshow("Image Processing",imgStacked)
            
            #cv.imshow('camera',frame)
            keyboard = cv.waitKey(30)
            if keyboard == 'q' or keyboard == 27:
                break
        except KeyboardInterrupt:
            break

    # cleanup
    capture.release()
    cv.destroyAllWindows()
    del capture
   os.system('sudo ip link set down can0') 
