from functions import *
import cv2 as cv

def graph_axis(frames, xs, start_frame):
    if len(frames[start_frame:]) >= 2:
        popt, pcov = curve_fit(axis, frames[start_frame:], xs[start_frame:])
    else:
        popt, pcov = curve_fit(axis, frames, xs)
    
    F = linspace(0, frames[-1], 1000)
    X = axis(F, popt[0], popt[1])
    clf()
    xlabel("frame number")
    ylabel("x position")
    plot(frames, xs)
    plot(F, X)
    show()

    return popt, pcov


def graph_vert(frames, ys, start_frame):
    if len(frames[start_frame:]) >= 3:
        popt, pcov = curve_fit(vert, frames[start_frame:], ys[start_frame:])
    else:
        popt, pcov = curve_fit(vert, frames, ys)
    
    F = linspace(0, frames[-1], 1000)
    Y = vert(F, popt[0], popt[1], popt[2])
    clf()
    xlabel("frame number")
    ylabel("y position")
    plot(frames, ys)
    plot(F, Y)
    show()

    return popt, pcov


def remove_outliers2(points):
    to_pop = []
    for i in range(len(points) - 2, 0, -1):
        x = points[i][0][0]
        x_prev = points[i-1][0][0]
        x_post = points[i+1][0][0]
        if not ((x > x_prev and x > x_post) or (x < x_prev and x < x_post)):
            to_pop.append(i+1)

    for i in to_pop:
        points.pop(i)

    
def scale_frame(frame, scale_percent):
    height, width = frame.shape[:2]
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    dim = (new_width, new_height)
    return cv.resize(frame, dim, interpolation = cv.INTER_AREA)


def find_first_frame_after_bounce(points):
    for i, point in enumerate(points):
        next_point = points[i+1]
        if next_point[0][1] < point[0][1]:
            return i