#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it published under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'

import sys
import locale

import cv2

locale.setlocale(locale.LC_TIME, '')
import time
from multiprocessing import Process, Queue, TimeoutError
from .utils.lines import make_face_line
from .utils.color import get_bgr_color


class Eyes(object):
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
        self.eyesCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye.xml')

        #        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1024)
        #        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 768)
        self.camera_source = 1
        self.video_capture = cv2.VideoCapture(self.camera_source)
        # self.video_capture.set(3,1080)
        # self.video_capture.set(4,1024)
        # self.video_capture.set(15, 0.1)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FPS, 5)

        self.frame_width = int(self.video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        self.line_width = 1

        self.color = 'green'
        self.valid_color_list = [
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'purple',
            'cyan'
        ]

    def run(self, queue):

        while True:

            try:

                ret, frame = self.video_capture.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Draw a rectangle around the eyes
                eyes = self.eyesCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=6,
                )
                for (ex, ey, ew, eh) in eyes:
                    cv2.circle(
                        frame,
                        (ex + (ew / 2), ey + (eh / 2)),
                        1,
                        get_bgr_color(color=self.color, lum=9),
                        -1,
                        cv2.CV_AA
                    )

                faces = self.faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.4,
                    minNeighbors=6,
                    minSize=(30, 30),
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )

                make_face_line(
                    faces,
                    frame,
                    self.frame_width,
                    self.frame_height,
                    skin='default',
                    color=self.color
                )


                # Draw Date at the button of the Video
                cv2.putText(
                    frame,
                    time.strftime('%d/%m/%Y %H:%M:%S'),
                    (int(1), int(self.frame_height - 4)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    get_bgr_color(color=self.color, lum=7),
                    2,
                    cv2.CV_AA
                )

                # Display the resulting frame
                cv2.imshow('Little Alice Eyes', frame)
                cv2.waitKey(1)
                # time.sleep(0.3)



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
