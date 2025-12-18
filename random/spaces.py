import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('Photos/cat.jpg')
cv.imshow('cat', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray', gray)

# to HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow('hsv', hsv)

# to LAB
lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)
cv.imshow('lab', lab)

rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

hsv_bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
cv.imshow('converted', hsv_bgr)

plt.imshow(rgb)
plt.show()

cv.waitKey(0)