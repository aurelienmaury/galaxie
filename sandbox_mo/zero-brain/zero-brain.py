#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amaury'

import os

import zmq
from brain import Brain

context = zmq.Context()

sock = context.socket(zmq.SUB)

ear_perceive_channel = ">ears>perceive>"

sock.setsockopt(zmq.SUBSCRIBE, ear_perceive_channel)
sock.connect("ipc:///tmp/zero_ears_bus")


brain_say_channel = ">brain>say>"
publish_sock = context.socket(zmq.PUB)
publish_sock.bind("ipc:///tmp/zero_brain_bus")

modules_dir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../little_alice/modules")
)

brains_dir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../little_alice/brains")
)

brain = Brain(modules_dir, brains_dir)

brain.load_brain()
brain.load_session()

try:
    while True:
        print "zero-brain subscribed to nervous system"
        message = sock.recv()
        print "receive "+message

        clean_message = message.replace(ear_perceive_channel, "", 1)

        brain_response = brain.kernel.respond(clean_message, brain.session_name)
        if brain_response:
            print "sending: "+brain_say_channel+brain_response
            publish_sock.send(brain_say_channel+brain_response)

        print "zero-brain did his job"
except KeyboardInterrupt:
    pass
finally:
    brain.save_session()