import cv2 as cv
img = cv.imread('Photos/cats.jpg')
cv.imshow('cat', img)

blur = cv.blur(img, (3,3))
cv.imshow('blur', blur)

gauss = cv.GaussianBlur(img, (3, 3), 0)
cv.imshow('blur2', gauss)

median = cv.medianBlur(img, 3)
cv.imshow('median', median)

bilateral = cv.bilateralFilter(img, 5, 15, 15)
cv.imshow('bilateral', bilateral)

cv.waitKey(0)
