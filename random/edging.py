import cv2 as cv
import numpy as np

img = cv.imread('Photos/cat.jpg')
cv.imshow('cat', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray', gray)

# Laplacian
lap = cv.Laplacian(gray, cv.CV_64F)
lap = np.uint8(np.absolute(lap))
cv.imshow('laplacian', lap)

#Sobel
sobelx = cv.Sobel(gray, cv.CV_64F, 1, 0)
sobely = cv.Sobel(gray, cv.CV_64F, 0, 1)
sobel = cv.bitwise_or(sobelx, sobely)
cv.imshow('x', sobelx)
cv.imshow('y', sobely)
cv.imshow('combined', sobel)


cv.waitKey(0)