import cv2 as cv
import numpy as np

img = cv.imread('Photos/cat.jpg')

cv.imshow('cat', img)

def translate(img, x, y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

tr = translate(img, -100, -100)
cv.imshow('trans', tr)

def rotate(img, angle, rotPoint=None):
    (height, width) = img.shape[:2]

    if not rotPoint:
        rotPoint = (width//2, height//2)
    
    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width, height)

    return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(img, 45, (50, 50))
cv.imshow('rot', rotated)

flip = cv.flip(img, 0)
cv.imshow('flip', flip)

cv.waitKey(0)