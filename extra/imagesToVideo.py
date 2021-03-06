import numpy as np
import cv2

cap = cv2.VideoCapture("../images/video/1_%08d.jpg") # 1_00000001.jpg

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        out.write(frame)
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
