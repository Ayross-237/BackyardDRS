import cv2 as cv
from helpers2 import * 

side_cam = cv.VideoCapture("https://192.168.0.11:8080/video")

while True:
    if cv.waitKey(1) & 0xff == ord('d'):
        break
    _, side = side_cam.read()

    # line to align with stump for side cam
    side = cv.line(side, (700, 0), (700, 1080), (0, 0, 255), 5)

    cv.imshow('side', scale_frame(side, 50))