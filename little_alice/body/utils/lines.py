__author__ = 'tuxa'

import cv2
from color import get_bgr_color


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
                get_bgr_color(color=color, lum=5),
                1,
                cv2.CV_AA
            )
            cv2.line(
                frame,
                (x + (w / 2), 0),
                (x + (w / 2), y),
                get_bgr_color(color=color, lum=5),
                line_width,
                cv2.CV_AA
            )
            cv2.line(
                frame,
                (x + (w / 2), y + h),
                (x + (w / 2), x + frame_height),
                get_bgr_color(color=color, lum=5),
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
                get_bgr_color(color=color, lum=9),
                1,
                cv2.CV_AA
            )
            cv2.line(
                frame,
                (0, y + (h / 2)),
                (x, y + (h / 2)),
                get_bgr_color(color=color, lum=5),
                line_width,
                cv2.CV_AA
            )
            cv2.line(
                frame,
                (x + w, y + (h / 2)),
                (y + frame_width, y + (w / 2)),
                get_bgr_color(color=color, lum=5),
                line_width,
                cv2.CV_AA
            )

            # Draw a rectangle around the faces
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                get_bgr_color(color=color, lum=8),
                line_width,
                cv2.CV_AA
            )
