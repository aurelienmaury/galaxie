#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amaury'

import zmq
import time
import os
from ears import Ears
import sys

context = zmq.Context()
sock = context.socket(zmq.SUB)
sock.setsockopt(zmq.SUBSCRIBE, ">ears>")
sock.connect("ipc:///tmp/little_alice_ears")

while True:
    message= sock.recv()
    print message
