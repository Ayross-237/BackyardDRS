import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from helpers2 import *
dist = lambda x1,x2,y1,y2: (x1-x2)**2 + (y1-y2)**2

HIT_DISTANCE = 150

class SideCam:
    def __init__(self, path: str, tennis_ball):
        self._vid = cv.VideoCapture(path) #Choose video file
        _, self._frame = self._vid.read()
        self._frame_num = 1
        self._prev_circle = None
        self._points = []
        self._tennis_ball = tennis_ball


    def next_frame(self):
        frame = self._frame[400:950, 500:1920]
        print(frame)
        b, g, r = cv.split(frame)
        blur = cv.GaussianBlur((r if self._tennis_ball else b), (13, 13), 0)

        circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=16, minRadius=10, maxRadius=30)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            chosen = None
            for i in circles[0, :]:
                if chosen is None: 
                    chosen = i
                if self._prev_circle is not None:
                    if dist(chosen[0], chosen[1], self._prev_circle[0], self._prev_circle[1]) <= dist(i[0], i[1], self._prev_circle[0], self._prev_circle[1]):
                        chosen = i
            if chosen[0] > HIT_DISTANCE + 50:
                self._points.append((chosen[:3], self._frame_num))
                cv.circle(frame, (chosen[0], chosen[1]), 1, (0, 0, 255), 3)
                cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)
                self._prev_circle = chosen

        # draw circles on frame
        print(self._points)
        for point in self._points:
            cv.circle(frame, point[0][:2], point[0][2], (255, 255, 255), 3)
        cv.circle(frame, (HIT_DISTANCE, 200), 20, (0, 0, 255), -1)
        cv.imshow('', frame)
        _, self._frame = self._vid.read()
        self._frame_num += 1
    

    def show_next_frame(self):
        frame = self._frame[400:950, 500:1920]
        cv.imshow('', frame)
        _, self._frame = self._vid.read()
        self._frame_num += 1
        return frame



    def get_hit_frame_info(self):
        frames = [point[1] for point in self._points]
        xs = [point[0][0] for point in self._points]
        ys = [point[0][1] for point in self._points]

        print(self._points)
        first_frame_after_bounce = find_first_frame_after_bounce(self._points)
        popt, _ = graph_axis(frames, xs, first_frame_after_bounce)
        y_popt, y_pcov = graph_vert(frames, ys, first_frame_after_bounce)
        further_frames = (axis_inv(HIT_DISTANCE, popt[0], popt[1]) - frames[-1]) * 2
        
        return further_frames, y_popt, y_pcov