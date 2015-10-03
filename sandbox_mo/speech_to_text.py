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
sock.bind("ipc:///tmp/little_alice_ears")

ears = Ears()

while True:

    print "ZERO LOOP:"
    recognizing = ears.decode_speech(
        ears.acoustic_model_directory,
        ears.language_model_file,
        ears.dictionary_file,
        ears.wavfile
    )

    print "RECONIZED:"+recognizing

    sock.send("ears:" + time.ctime() + ":" + recognizing)
