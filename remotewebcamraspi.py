# Uses "motion" on raspberry pi as a webcam server
# sudo modprobe bcm2835-v4l2 if it works you should get a /dev/video0
import cv2
import numpy as np
import arucotracking

cap = cv2.VideoCapture("http://192.168.0.14:8081")

while(True):
    ret, frame = cap.read()
    # cv2.imshow('frame',frame)
    arucotracking.track(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
