import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img = cv.imread('Photos/cat.jpg')
cv.imshow('cat', img)

blank = np.zeros(img.shape[:2], dtype='uint8')
cv.imshow('blank', blank)

mask = cv.circle(blank, (img.shape[1]//2, img.shape[0]//2), 100, 255, -1)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('gray', gray)

gray_hist = cv.calcHist([gray], [0], mask, [256], [0,256])

plt.figure()
plt.title('Grayscale Histogram')
plt.xlabel('Bins')
plt.plot(gray_hist)
plt.xlim([0,256])
plt.show()

cv.waitKey(0)
