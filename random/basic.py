import cv2 as cv

img = cv.imread('Photos/cat.jpg')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray', gray)

blur = cv.GaussianBlur(img, (3, 3), cv.BORDER_DEFAULT)
cv.imshow('blur', blur)

canny = cv.Canny(img, 125, 175)
cv.imshow('canny', canny)

resized = cv.resize(img, (250, 250))
cv.imshow('resized', resized)

cropped = img[50:200, 200:400]
cv.imshow('cropped', cropped)

cv.waitKey(0)