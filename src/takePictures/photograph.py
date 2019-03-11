import cv2
from cv2 import VideoCapture
import datetime
import os

def take_photoes(_dir):
    while True:
        ret, frame = cap.read()
        # Our operations on the frame come here

        # Display the resulting frame
        cv2.imshow('frame',frame)
        c = cv2.waitKey(1)
        if c == ord('q'):
            break
        if c == ord('s'):
            path = os.path.join(_dir,time_as_name())
            cv2.imwrite(path,frame)

def time_as_name():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S.jpg")

if __name__ == '__main__':
    cap = VideoCapture(0)
    cap.set(3,2048)
    cap.set(4,1536)
    # cap.set(3,1600)
    # cap.set(4,1200)
    take_photoes("new")
    cap.release()
    cv2.destroyAllWindows()



