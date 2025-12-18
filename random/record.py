import cv2 as cv
import os 
file_path = 'Videos/sample.mp4'

video = cv.VideoCapture(1)


while True:
    isTrue, frame = video.read()
    cv.imshow('feed', frame)

    if cv.waitKey(1) & 0xff == ord('d'):
        break

    print(frame.shape)
def remove_file(file_path):
    try: 
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")

    except FileNotFoundError: 
        print(f"File '{file_path}' not found.")