import cv2 as cv
dist = lambda x1,x2,y1,y2: (x1-x2)**2 + (y1-y2)**2

def set_constants(frame) -> None:
    if frame.shape[0] == 3840:
        BLUR_SQR_SIZE = 19
        MAX_RADIUS = 30
        MIN_RADIUS = 5
        PARAM1 = 100
        PARAM2 = 30
        HIT_RADIUS = 17
    elif frame.shape[0] == 1920:
        BLUR_SQR_SIZE = 13
        MAX_RADIUS = 15
        MIN_RADIUS = 0
        PARAM1 = 100
        PARAM2 = 20
        HIT_RADIUS = 7.5
    else:
        raise ValueError("does not fit sizes")
    return BLUR_SQR_SIZE, MAX_RADIUS, MIN_RADIUS, PARAM1, PARAM2, HIT_RADIUS


def resize_frame(frame):
    if frame.shape[0] == 3840:
        frame = frame[1800:2800, 500:1350]
    elif frame.shape[0] == 1920:
        frame = frame[800:1300, 200:675]
    return frame


def remove_outliers(points):
    to_pop = []
    for i in range(1, len(points) - 1):
        x1, y1 = points[i-1][0][:2]
        x2, y2 = points[i][0][:2]
        x3, y3 = points[i+1][0][:2]

        if abs(dist(x1, x2, y1, y2)) > 5000000 and abs(dist(x2, x3, y2, y3)) > 5000000:
            to_pop.append(i)

    for i in to_pop[::-1]:
        points.pop(i)


def find_first_frame_after_bounce(points):
    for i, point in enumerate(points):
        next_point = points[i+1]
        print(next_point[0][1] < point[0][1])
        if next_point[0][1] < point[0][1]:
            return i
    