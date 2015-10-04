#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amaury'

import zmq
import os
import sys

brain_say_channel = ">brain>say>"
context = zmq.Context()
sock = context.socket(zmq.SUB)
sock.setsockopt(zmq.SUBSCRIBE, brain_say_channel)
sock.connect("ipc:///tmp/zero_brain_bus")

def get_app_path(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

def espeack_path():
    if not get_app_path('espeak'):
        print "Error: Espeack is require, for enable voice"
        print "Error: Please install \"espeak\" or verify it is aviable on your $PATH env var"
        sys.exit(1)
    else:
        return get_app_path('espeak')

def mbrola_path():
    if not get_app_path('mbrola'):
        print "Error: Mbrola is require, for enable voice"
        print "Error: Please install \"mbrola\" or verify it is aviable on your $PATH env var"
        sys.exit(1)
    else:
        return get_app_path('mbrola')

def soxplay_path():
    if not get_app_path('play'):
        print "Error: Sox tool is require, for enable voice"
        print "Error: Please install \"Sox Player\" or verify it is aviable on your $PATH env var"
        sys.exit(1)
    else:
        return get_app_path('play')

text_to_speech_command_line = espeack_path() + ' -v mb/mb-fr4 -q -s150  --pho --stdout \"%s\"'
text_to_speech_command_line += ' | '
text_to_speech_command_line += mbrola_path() + ' -t 1.2 -f 1.4 -e /usr/share/mbrola/fr4/fr4 - -.au'
text_to_speech_command_line += ' | '
text_to_speech_command_line += soxplay_path() + ' -t au - bass +1 pitch -300 echo 0.8 0.4 99 0.3'

while True:
    print "zero-voice subscribed to nervous system"

    message = sock.recv()

    clean_message = message.replace(brain_say_channel, "", 1)

    if clean_message:
        os.system(text_to_speech_command_line % clean_message)

    print "text_to_speech: "+clean_message
    print "zero-voice did his job"
