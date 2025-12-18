import cv2 as cv

capture = cv.VideoCapture(0)

while True:
    isTrue, frame = capture.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 7, 5)
    cv.imshow('adaptive', adaptive_thresh)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break
