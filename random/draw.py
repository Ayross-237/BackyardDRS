import cv2 as cv
import numpy as np

#blank = np.zeros((500,500, 3), dtype='uint8')

#img = cv.imread('Photos/cat.jpg')
capture = cv.VideoCapture(0)

#blank[200:300, 300:400] = 0,255,0
#cv.rectangle(blank, (0, 0), (250, 250), (0, 255, 0), thickness=2)
#cv.circle(blank, (250, 250), 40, (0, 0, 255), thickness= 3)
#cv.line(blank, (0, 0), (250, 250), (255, 255, 255), thickness=3)
#cv.putText(blank, 'Hello', (255, 255), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0, 255, 0), 2)
#cv.imshow('Green', blank)

cuz = lambda x: int(0.01*x**2)

x = -250

coords = []
while True:
    isTrue, frame = capture.read()
    coords.append((x +  250, cuz(x)))
    x += 1
    
    for coord in coords:
        cv.circle(frame, coord, 5, (255, 255, 255), thickness=2)

    cv.imshow('Video', cv.Canny(frame, 125, 175))

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

cv.waitKey(0)


