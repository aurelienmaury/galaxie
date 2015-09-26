#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'

import cv2
import sys

from multiprocessing import TimeoutError


class Eyes(object):
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
        self.eyesCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye.xml')
        self.video_capture = cv2.VideoCapture(0)
#        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1024)
#        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 768)

    def run(self, queue):
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
                cv2.imshow('Alice Eyes', frame)
                cv2.waitKey(1)



            except KeyboardInterrupt:
                sys.exit(0)

            except TimeoutError:
                cv2.destroyAllWindows()

            except:
                self.video_capture.release()
                cv2.destroyAllWindows()

    def terminate(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
