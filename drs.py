import sys
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from functions import *
from helpers import *
from side_cam import *

test_num = sys.argv[1] if len(sys.argv) > 1 else '7'
tennis_ball = sys.argv[2] == 1 if len(sys.argv) > 2 else '1'
side_cam = SideCam(f'Tests/{test_num}/side.mp4', tennis_ball)
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

    blur = cv.GaussianBlur((r if tennis_ball else b), (BLUR_SQR_SIZE, BLUR_SQR_SIZE), 0)
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

    # keep the 120fps and 60fps videos aligned
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
xs = [point[0][0] for point in points]

first_frame_after_bounce = find_first_frame_after_bounce(points)
x_popt, x_pcov = curve_fit(axis, frames[first_frame_after_bounce:], xs[first_frame_after_bounce:], p0=[1, 1])

# plot graph
F = np.linspace(1, frames[-1], 100)
X = axis(F, x_popt[0], x_popt[1])
clf()
xlabel("frame number")
ylabel("x position")
plot(frames, xs)
plot(F, X)
show()

last_side_frame = None
while isTrue:
    frame = resize_frame(frame)
    last_frame = frame.copy()
    if cv.waitKey(0) & 0xFF == ord('d'):
        break
    if frame_num % 2 == 0:
        last_side_frame = side_cam.show_next_frame()
    cv.imshow('Ball Tracking', scale_frame(frame, 150))
    isTrue, frame = vid.read()
    frame_num += 1

vid.release()
cv.destroyAllWindows()

hit_frame, y_popt, y_pcov = side_cam.get_hit_frame_info()
hit_frame += frames[-1]

x = int(axis([hit_frame], x_popt[0], x_popt[1])[0])
y = int(vert([hit_frame//2 + 1], y_popt[0], y_popt[1], y_popt[2])[0])

cv.rectangle(last_frame, (x, 0), (x, 1000), (0, 0, 255))
cv.rectangle(last_side_frame, (0, y), (1920, y), (0, 0, 255))

plt.imshow(scale_frame(cv.cvtColor(last_frame, cv.COLOR_BGR2RGB), 150))
plt.show()
plt.imshow(cv.cvtColor(last_side_frame, cv.COLOR_BGR2RGB))
plt.show()