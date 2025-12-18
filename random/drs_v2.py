import sys
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from regression import *
from helpers import *
from side_cam import *
import time

test_num = sys.argv[1]
print(test_num)

side_cam = SideCam(f'Tests/{test_num}/side.mp4')
vid = cv.VideoCapture(f'Tests/{test_num}/ball.mp4') #Choose video file

prev_circle = None
points = []

isTrue, frame = vid.read()
BLUR_SQR_SIZE, MAX_RADIUS, MIN_RADIUS, PARAM1, PARAM2, HIT_RADIUS = set_constants(frame)
frame_num = 1
last_frame = None

while isTrue:
    frame = resize_frame(frame)
    last_frame = frame.copy()
    b, g, r = cv.split(frame)
    
    if cv.waitKey(0) & 0xFF == ord('d'):
        break

    blur = cv.GaussianBlur(r, (BLUR_SQR_SIZE, BLUR_SQR_SIZE), 0)
    circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1.2, 100, param1=PARAM1, param2=PARAM2, minRadius=MIN_RADIUS, maxRadius=MAX_RADIUS)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None: 
                chosen = i
            if prev_circle is not None:
                if dist(chosen[0], chosen[1], prev_circle[0], prev_circle[1]) <= dist(i[0], i[1], prev_circle[0], prev_circle[1]):
                    chosen = i
        points.append((chosen[:3], frame_num))
        cv.circle(frame, (chosen[0], chosen[1]), 1, (0, 0, 255), 3)
        prev_circle = chosen

    # draw circles on frame
    for point in points:
        cv.circle(frame, point[0][:2], point[0][2], (255, 255, 255), 3)

    if frame_num % 2 == 0:
        side_cam.next_frame()
    
    cv.imshow('Ball Tracking', scale_frame(frame, 150))
    isTrue, frame = vid.read()
    frame_num += 1

cv.destroyAllWindows()

cv.waitKey(0)
side_cam.remove_outliers()
remove_outliers(points)
frames = [point[1] for point in points]
radii = [point[0][2] for point in points]

first_frame_after_bounce = find_first_frame_after_bounce(points)

xs = [point[0][0] for point in points]
ys = [point[0][1] for point in points]

d_popt, d_pcov = curve_fit(depth, frames, radii, p0=[0.1, 0])
x_popt, x_pcov = curve_fit(axis, frames[first_frame_after_bounce:], xs[first_frame_after_bounce:], p0=[1, 1])
y_popt, y_popv = curve_fit(vert, frames[first_frame_after_bounce:], ys[first_frame_after_bounce:], p0=[0.1, 1, 100])

F = np.linspace(1, frames[-1], 100)
X = axis(F, x_popt[0], x_popt[1])
Y = vert(F, y_popt[0], y_popt[1], y_popt[2])

# plot graphs
clf()
plot(frames, xs)
plot(F, X)
plot(frames, ys)
plot(F, Y)
show()

while isTrue:
    frame = resize_frame(frame)
    last_frame = frame.copy()
    if cv.waitKey(0) & 0xFF == ord('d'):
        break
    if frame_num % 2 == 0:
        side_cam.show_next_frame()
    cv.imshow('Ball Tracking', scale_frame(frame, 150))
    isTrue, frame = vid.read()
    frame_num += 1

vid.release()
cv.destroyAllWindows()

hit_frame = frames[-1] + side_cam.get_hit_frame()
x = int(axis([hit_frame], x_popt[0], x_popt[1])[0])
y = int(vert([hit_frame], y_popt[0], y_popt[1], y_popt[2])[0])
cv.circle(last_frame, (x, y), int(HIT_RADIUS), (0, 0, 255), -1)
cv.circle(last_frame, (x, y), 3, (255, 255, 255), -1)

plt.imshow(scale_frame(cv.cvtColor(last_frame, cv.COLOR_BGR2RGB), 150))
plt.show()