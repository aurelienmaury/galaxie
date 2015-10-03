#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'amaury'

import argparse

parser = argparse.ArgumentParser(description='Event piping through 0MQ')

parser.add_argument('--from', help='0MQ upstream')
parser.add_argument('--sub', type=str, help='act as subscriber to value')
parser.add_argument('--pull', type=str, help='act as puller')

args = parser.parse_args()

import zmq
import time

# ZeroMQ Context

context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.PUB)
sock.bind("ipc:///tmp/zerolab")

id = 0

while True:
    time.sleep(1)
    id, now = id+1, time.ctime()

    # Message [prefix][message]
    message = "pub: Update! >> #{id} >> {time}".format(id=id, time=now)
    sock.send(message)
