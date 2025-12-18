import cv2 as cv

video = cv.VideoCapture(0)

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def changeRes(width, height): #only works for live video
    video.set(3, width)
    video.set(4, height)

changeRes(1080, 720)
while True:
    isTrue, frame = video.read()
    cv.imshow('cat', rescaleFrame(frame, 2.5))

    if cv.waitKey(5) & 0xFF == ord('d'):
        break


video.release()
cv.destroyAllWindows()