#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amaury'

import zmq
import time
import os
from ears import Ears

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.PUB)
sock.bind("ipc:///tmp/zero_ears_bus")

ears = Ears(sock)

while True:
    print "zero-ears up"
    sock.send(">ears>prompt>type=1")

    recognizing = ears.decode_speech(
        ears.acoustic_model_directory,
        ears.language_model_file,
        ears.dictionary_file,
        ears.wavfile
    )

    if recognizing:
        print "zero-ears perceive "+recognizing
        message = ">ears>perceive>" + recognizing
        sock.send(message)
