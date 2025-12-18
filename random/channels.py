import cv2 as cv
import numpy as np

img = cv.imread('Photos/cat.jpg')
cv.imshow('Boston', img)

b, g, r = cv.split(img)

blank = np.zeros(img.shape[:2], dtype='uint8')

blue = cv.merge([b, blank, blank])
green = cv.merge([blank, g, blank])
red = cv.merge([blank, blank, r])

cv.imshow('g', green)

cv.waitKey(0)

