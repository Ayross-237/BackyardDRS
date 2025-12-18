import cv2 as cv
import numpy as np

img = cv.imread('Photos/cat.jpg')

cv.imshow('Cats', img)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

cv.imshow('gray', gray)

canny = cv.Canny(img, 125, 175)
cv.imshow('canny', canny)

ret, thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
cv.imshow('thresh', thresh)

blank = np.zeros(img.shape, dtype='uint8')
cv.imshow('blank', blank)

contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

cv.drawContours(blank, contours, -1, (0, 0, 255), 1)
cv.imshow('contours', blank)
cv.waitKey(0)