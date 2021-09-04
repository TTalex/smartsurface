import urllib.request
import cv2
import numpy as np
import time
import arucotracking

URL = "http://192.168.0.10:8080/shot.jpg"

while True:
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    # cv2.imshow('IPwebcam', img)
    arucotracking.track(img)
    cv2.waitKey(1)
