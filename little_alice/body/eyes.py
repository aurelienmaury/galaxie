#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'


import cv2
import sys
import locale
locale.setlocale(locale.LC_TIME, '')
import time

from multiprocessing import TimeoutError

# Tango Palette Color
TANGO_PALETTE_GREY = (83, 87, 85)
TANGO_PALETTE_RED = (41, 41, 239)
TANGO_PALETTE_GREEN = (52, 226, 138)
TANGO_PALETTE_YELLOW = (79, 233, 252)
TANGO_PALETTE_BLUE = (207, 159, 114)
TANGO_PALETTE_PURPLE = (168, 127, 173)
TANGO_PALETTE_CYAN_9 = (252, 252, 58)
TANGO_PALETTE_CYAN_8 = (226, 226, 52)
TANGO_PALETTE_CYAN_7 = (201, 201, 46)
TANGO_PALETTE_CYAN_6 = (176, 176, 40)
TANGO_PALETTE_CYAN_5 = (150, 150, 35)
TANGO_PALETTE_CYAN_4 = (125, 125, 29)
TANGO_PALETTE_CYAN_3 = (99, 99, 23)
TANGO_PALETTE_CYAN_2 = (79, 79, 17)
TANGO_PALETTE_CYAN_1 = (48, 48, 11)
TANGO_PALETTE_CYAN_0 = (23, 23, 5)

class Eyes(object):
    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
        self.eyesCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye.xml')

#        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1024)
#        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 768)
        self.camera_source = 0
        self.video_capture = cv2.VideoCapture(self.camera_source)
        #self.video_capture.set(3,1080)
        #self.video_capture.set(4,1024)
        #self.video_capture.set(15, 0.1)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FPS, 5)

        self.frame_width = int(self.video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        self.line_width = 1

    def run(self, queue):

        while True:
            try:
                ret, frame = self.video_capture.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #frame = cv2.flip(frame, 1)

                faces = self.faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=6,
                    minSize=(30, 30),
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )

                for (x, y, w, h) in faces:
                    # Draw X Lines
                    cv2.putText(
                        frame,
                        str(int(x + (w/2))),
                        (x + (w/2) + 1, 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        TANGO_PALETTE_CYAN_9,
                        1,
                        cv2.CV_AA
                    )
                    cv2.line(
                        frame,
                        (x + (w/2), 0),
                        (x + (w/2), y),
                        TANGO_PALETTE_CYAN_5,
                        self.line_width,
                        cv2.CV_AA
                    )
                    cv2.line(
                        frame,
                        (x + (w/2), y+h),
                        (x + (w/2), x+self.frame_height),
                        TANGO_PALETTE_CYAN_5,
                        self.line_width,
                        cv2.CV_AA
                    )

                    # Draw Y Lines
                    cv2.putText(
                        frame,
                        str(int(y + (h/2))),
                        (int(2), int(y + (h/2) - 2)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        TANGO_PALETTE_CYAN_9,
                        1,
                        cv2.CV_AA
                    )
                    cv2.line(
                        frame,
                        (0, y + (h/2)),
                        (x, y + (h/2)),
                        TANGO_PALETTE_CYAN_5,
                        self.line_width,
                        cv2.CV_AA
                    )
                    cv2.line(
                        frame,
                        (x+w, y + (h/2)),
                        (y+self.frame_width, y + (w/2)),
                        TANGO_PALETTE_CYAN_5,
                        self.line_width,
                        cv2.CV_AA
                    )

                    # Draw a rectangle around the faces
                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x+w, y+h),
                        TANGO_PALETTE_CYAN_8,
                        self.line_width,
                        cv2.CV_AA
                    )

                    # Draw a rectangle around the eyes
                    eyes = self.eyesCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.2,
                        minNeighbors=6,
                    )
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(
                            frame,
                            (ex, ey),
                            (ex+ew, ey+eh),
                            TANGO_PALETTE_CYAN_6,
                            1,
                            cv2.CV_AA
                        )


                # Draw Date at the button of the Video
                cv2.putText(
                    frame,
                    time.strftime('%d/%m/%Y %H:%M:%S'),
                    (int(1), int(self.frame_height - 4)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    TANGO_PALETTE_CYAN_7,
                    2,
                    cv2.CV_AA
                )


                # Display the resulting frame
                cv2.imshow('Merdouille', frame)
                cv2.waitKey(1)
                #time.sleep(0.3)



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
