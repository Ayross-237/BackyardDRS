import cv2 as cv
import matplotlib.pyplot as plt

vid = cv.VideoCapture('Videos/ball.mp4')

_, frame = vid.read()

plt.imshow(frame)
plt.show()