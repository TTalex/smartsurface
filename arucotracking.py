"""
An example of detecting ArUco markers with OpenCV.
"""

import cv2
import sys
import cv2.aruco as aruco
import numpy as np
from scipy.spatial import distance
import json
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)


last_values = {}
def track(frame):
    # Convert from BGR to RGB
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    frame = aruco.drawDetectedMarkers(frame, corners, ids)
    # cv2.imshow('frame', frame)
    if np.all(ids != None):
        maintopleft = None
        maintopright = None
        mainbottomleft = None
        mainbottomright = None
        for corner, id in zip(corners, ids):
            topleft = (corner[0][0][0], corner[0][0][1])
            # topright = (corner[0][1][0], corner[0][1][1])
            bottomright = (corner[0][2][0], corner[0][2][1])
            center = (int((bottomright[0]+topleft[0]) / 2), int((bottomright[1]+topleft[1]) / 2))
            if (id[0] == 0):
                maintopleft = center
            if (id[0] == 1):
                maintopright = center
            if (id[0] == 2):
                mainbottomleft = center
            if (id[0] == 3):
                mainbottomright = center
            # radius = int(distance.euclidean(topleft, topright)/2)
            # cv2.circle(frame, first_center, radius, (0,0,255), 10)
        if not (maintopleft and maintopright and mainbottomleft and mainbottomright):
            return
        h, status = cv2.findHomography(np.array([maintopleft, maintopright, mainbottomright, mainbottomleft]), np.array([[0,0], [1000,0], [1000,1000], [0,1000]]))
        for corner, id in zip(corners, ids):
            if (id[0] > 3):
                topleft = (corner[0][0][0], corner[0][0][1])
                bottomright = (corner[0][2][0], corner[0][2][1])
                center = [int((bottomright[0]+topleft[0]) / 2), int((bottomright[1]+topleft[1]) / 2)]
                pts = np.float32(center).reshape(-1,1,2)
                relative_center = cv2.perspectiveTransform(pts, h)[0][0]
                # relative_center = (
                #     (center[0] - mins[0]) / (maxs[0] - mins[0]) * 1000,
                #     (center[1] - mins[1]) / (maxs[1] - mins[1]) * 1000
                # )
                print(id[0], relative_center)
                if (id[0] not in last_values) or (abs(last_values[id[0]][0] - relative_center[0]) > 10 and abs(last_values[id[0]][1] - relative_center[1]) > 10):
                    print("significant move")
                    client.publish("aruco", json.dumps({"id": int(id[0]), "x": float(relative_center[0]), "y": float(relative_center[1])}))
                last_values[id[0]] = relative_center

        # im_out = cv2.warpPerspective(frame, h, (1000,600))
        # cv2.imshow('out', im_out)
    # Display the resulting frame
    # cv2.imshow('frame', frame)
