#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'


def get_bgr_color(color=None, lum=8):
    # Definition return 10 varition from Drak=0 to Liht=10
    # Tango Palette Color for Terminal Console
    color_grey = (83, 87, 85)
    color_red = (41, 41, 239)
    color_green = (52, 226, 138)
    color_yellow = (79, 233, 252)
    color_blue = (207, 159, 114)
    color_purple = (168, 127, 173)
    color_cyan = (226, 226, 52)

    valid_color_list = [
        'grey',
        'red',
        'green',
        'yellow',
        'blue',
        'purple',
        'cyan'
    ]
    found = 0
    for color_item in valid_color_list:
        if color == color_item:
            found = not found

    if not found:
        color = 'cyan'

    if color == 'grey':
        if lum == 0:
            return 22, 23, 22
        elif lum == 1:
            return 46, 48, 47
        elif lum == 2:
            return 71, 74, 72
        elif lum == 3:
            return 95, 99, 97
        elif lum == 4:
            return 119, 125, 122
        elif lum == 5:
            return 144, 150, 147
        elif lum == 6:
            return 168, 176, 172
        elif lum == 7:
            return 192, 201, 197
        elif lum == 8:
            return 217, 227, 222
        elif lum == 9:
            return 241, 252, 247
        else:
            return 243, 255, 249
    if color == 'red':
        if lum == 0:
            return 4, 4, 23
        elif lum == 1:
            return 8, 8, 48
        elif lum == 2:
            return 13, 13, 74
        elif lum == 3:
            return 17, 17, 99
        elif lum == 4:
            return 21, 21, 125
        elif lum == 5:
            return 26, 26, 150
        elif lum == 6:
            return 30, 30, 176
        elif lum == 7:
            return 35, 35, 201
        elif lum == 8:
            return 39, 39, 227
        elif lum == 9:
            return 43, 43, 252
        else:
            return 44, 44, 255
    if color == 'green':
        if lum == 0:
            return 5, 23, 14
        elif lum == 1:
            return 11, 48, 11
        elif lum == 2:
            return 17, 74, 17
        elif lum == 3:
            return 23, 99, 23
        elif lum == 4:
            return 29, 125, 29
        elif lum == 5:
            return 35, 150, 35
        elif lum == 6:
            return 40, 176, 40
        elif lum == 7:
            return 46, 201, 46
        elif lum == 8:
            return 52, 227, 52
        elif lum == 9:
            return 58, 252, 58
        else:
            return 58, 255, 58
    if color == 'yellow':
        if lum == 0:
            return 7, 21, 23
        elif lum == 1:
            return 15, 45, 48
        elif lum == 2:
            return 23, 68, 74
        elif lum == 3:
            return 31, 92, 99
        elif lum == 4:
            return 39, 115, 125
        elif lum == 5:
            return 47, 138, 150
        elif lum == 6:
            return 55, 162, 176
        elif lum == 7:
            return 63, 186, 201
        elif lum == 8:
            return 71, 209, 227
        elif lum == 9:
            return 79, 233, 252
        else:
            return 80, 236, 255
    if color == 'blue':
        if lum == 0:
            return 23, 18, 13
        elif lum == 1:
            return 48, 37, 27
        elif lum == 2:
            return 74, 57, 41
        elif lum == 3:
            return 99, 76, 55
        elif lum == 4:
            return 125, 96, 69
        elif lum == 5:
            return 150, 116, 83
        elif lum == 6:
            return 176, 135, 97
        elif lum == 7:
            return 201, 155, 111
        elif lum == 8:
            return 227, 174, 125
        elif lum == 9:
            return 252, 194, 139
        else:
            return 255, 196, 140
    if color == 'purple':
        if lum == 0:
            return 22, 17, 23
        elif lum == 1:
            return 47, 36, 48
        elif lum == 2:
            return 72, 54, 72
        elif lum == 3:
            return 97, 73, 99
        elif lum == 4:
            return 121, 92, 125
        elif lum == 5:
            return 146, 110, 150
        elif lum == 6:
            return 171, 129, 176
        elif lum == 7:
            return 196, 148, 201
        elif lum == 8:
            return 220, 167, 227
        elif lum == 9:
            return 245, 185, 252
        else:
            return 248, 187, 255
    if color == 'cyan':
        if lum == 0:
            return 23, 23, 5
        elif lum == 1:
            return 48, 48, 11
        elif lum == 2:
            return 79, 79, 17
        elif lum == 3:
            return 99, 99, 23
        elif lum == 4:
            return 125, 125, 29
        elif lum == 5:
            return 150, 150, 35
        elif lum == 6:
            return 176, 176, 40
        elif lum == 7:
            return 201, 201, 46
        elif lum == 8:
            return 226, 226, 52
        elif lum == 9:
            return 252, 252, 58
        else:
            return 255, 255, 59

