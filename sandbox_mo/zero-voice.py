#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amaury'

import zmq
import time
import os
from ears import Ears
import sys
from voice import Voice

context = zmq.Context()
sock = context.socket(zmq.SUB)
sock.setsockopt(zmq.SUBSCRIBE, ">brain>say>")
sock.connect("ipc:///tmp/zero_brain_bus")

voice = Voice()

while True:
    print "zero-voice subscribed to nervous system"
    message = sock.recv()
    clean_message = message.replace(">brain>say>", "", 1)
    voice.text_to_speech(clean_message)
    print "zero-voice did his job"
