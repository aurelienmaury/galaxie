#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it published under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'

import time
import locale
import cv2

locale.setlocale(locale.LC_TIME, '')

PALETTE = {
    'grey': {0: (22, 23, 22), 1: (46, 48, 47), 2: (71, 74, 72), 3: (95, 99, 97), 4: (119, 125, 122), 5: (144, 150, 147),
             6: (168, 176, 172), 7: (192, 201, 197), 8: (217, 227, 222), 9: (241, 252, 247), 10: (243, 255, 249)},
    'red': {0: (4, 4, 23), 1: (8, 8, 48), 2: (13, 13, 74), 3: (17, 17, 99), 4: (21, 21, 125), 5: (26, 26, 150),
            6: (30, 30, 176), 7: (35, 35, 201), 8: (39, 39, 227), 9: (43, 43, 252), 10: (44, 44, 255)},
    'green': {0: (5, 23, 14), 1: (11, 48, 11), 2: (17, 74, 17), 3: (23, 99, 23), 4: (29, 125, 29), 5: (35, 150, 35),
              6: (40, 176, 40), 7: (46, 201, 46), 8: (52, 227, 52), 9: (58, 252, 58), 10: (58, 255, 58)},
    'yellow': {0: (7, 21, 230), 1: (15, 45, 48), 2: (23, 68, 74), 3: (31, 92, 99), 4: (39, 115, 125), 5: (47, 138, 150),
               6: (55, 162, 176), 7: (63, 186, 201), 8: (71, 209, 227), 9: (79, 233, 252), 10: (80, 236, 255)},
    'blue': {0: (23, 18, 13), 1: (48, 37, 27), 2: (74, 57, 41), 3: (99, 76, 55), 4: (125, 96, 69), 5: (150, 116, 83),
             6: (176, 135, 97), 7: (201, 155, 111), 8: (227, 174, 125), 9: (252, 194, 139), 10: (255, 196, 140)},
    'purple': {0: (22, 17, 23), 1: (47, 36, 48), 2: (72, 54, 72), 3: (97, 73, 99), 4: (121, 92, 125),
               5: (146, 110, 150), 6: (171, 129, 176), 7: (196, 148, 201), 8: (220, 167, 227), 9: (245, 185, 252),
               10: (248, 187, 255)},
    'cyan': {0: (23, 23, 5), 1: (48, 48, 11), 2: (79, 79, 17), 3: (99, 99, 23), 4: (125, 125, 29), 5: (150, 150, 35),
             6: (176, 176, 40), 7: (201, 201, 46), 8: (226, 226, 52), 9: (252, 252, 58), 10: (255, 255, 59)}
}

def make_face_line(faces, frame, frame_width, frame_height, skin='default', color=None, line_width=1):
    if skin == 'default':
        for (x, y, w, h) in faces:
            # Draw X Lines
            cv2.putText(
                frame,
                str(int(x + (w / 2))),
                (x + (w / 2) + 1, 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                PALETTE[color][5],
                1,
                cv2.CV_AA
            )
            cv2.line(
                frame,
                (x + (w / 2), 0),
                (x + (w / 2), y),
                PALETTE[color][5],
                line_width,
                cv2.CV_AA
            )
            cv2.line(
                frame,
                (x + (w / 2), y + h),
                (x + (w / 2), x + frame_height),
                PALETTE[color][5],
                line_width,
                cv2.CV_AA
            )

            # Draw Y Lines
            cv2.putText(
                frame,
                str(int(y + (h / 2))),
                (int(2), int(y + (h / 2) - 2)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                PALETTE[color][9],
                1,
                cv2.CV_AA
            )
            cv2.line(
                frame,
                (0, y + (h / 2)),
                (x, y + (h / 2)),
                PALETTE[color][5],
                line_width,
                cv2.CV_AA
            )
            cv2.line(
                frame,
                (x + w, y + (h / 2)),
                (y + frame_width, y + (w / 2)),
                PALETTE[color][5],
                line_width,
                cv2.CV_AA
            )

            # Draw a rectangle around the faces
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                PALETTE[color][8],
                line_width,
                cv2.CV_AA
            )


faceCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
eyesCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye.xml')
camera_source = 1
video_capture = cv2.VideoCapture(camera_source)
video_capture.set(cv2.cv.CV_CAP_PROP_FPS, 5)

frame_width = int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
line_width = 1

color = 'green'

try:
    while True:
        print "zero-eyes loop"

        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Draw a rectangle around the eyes
        eyes = eyesCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, )

        for (ex, ey, ew, eh) in eyes:
            cv2.circle(
                frame,
                (ex + (ew / 2), ey + (eh / 2)),
                1,
                PALETTE[color][9],
                -1,
                cv2.CV_AA
            )

        # detect faces and rectangle them
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.4,
            minNeighbors=6,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        make_face_line(
            faces,
            frame,
            frame_width,
            frame_height,
            skin='default',
            color=color
        )

        # Draw Date at the button of the Video
        cv2.putText(
            frame,
            time.strftime('%d/%m/%Y %H:%M:%S'),
            (int(1), int(frame_height - 4)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            PALETTE[color][7],
            2,
            cv2.CV_AA
        )

        # Display the resulting frame
        cv2.imshow('Little Alice Eyes', frame)
        cv2.waitKey(1)

except KeyboardInterrupt:
    pass
finally:
    video_capture.release()
    cv2.destroyAllWindows()
