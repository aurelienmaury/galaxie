#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amaury'

import zmq
import time

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.PUB)
sock.bind("ipc:///tmp/zero_ears_bus")

while True:
    print "zero-ears up"
    sock.send(">ears>prompt>type=1")

    time.sleep(3)
    recognizing = "bonjour"
    print "zero-ears perceive "+recognizing
    message = ">ears>perceive>" + recognizing
    sock.send(message)
