#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amaury'

import zmq
import sys

context = zmq.Context()
sock = context.socket(zmq.SUB)
sock.setsockopt(zmq.SUBSCRIBE, "")
sock.connect(sys.argv[1])

while True:
    message = sock.recv()
    print message
