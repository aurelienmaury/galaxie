# -*- coding: utf-8 -*-
__author__ = 'tuxa'

import cv2
import sys

from multiprocessing import TimeoutError

class Eyes(object):
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
        self.eyesCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye.xml')
        self.video_capture = cv2.VideoCapture(1)

    def look(self, queue):
        while True:
            try:
                ret, frame = self.video_capture.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = self.faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )

                # Draw a rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    eyes = self.eyesCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(eyes, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

                # Display the resulting frame
                cv2.imshow('Video', frame)
                cv2.waitKey(1)

            except KeyboardInterrupt:
                sys.exit(0)

            except TimeoutError:
                cv2.destroyAllWindows()