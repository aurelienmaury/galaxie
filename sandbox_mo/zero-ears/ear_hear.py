#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amaury'


import zmq
import sys
import time

context = zmq.Context()

brain_say_channel = ">ears>perceive>"
publish_sock = context.socket(zmq.PUB)
publish_sock.bind("ipc:///tmp/zero_ears_bus")


publish_sock.send(brain_say_channel+"bonjour")
time.sleep(3)
publish_sock.send(brain_say_channel+sys.argv[1])
time.sleep(3)