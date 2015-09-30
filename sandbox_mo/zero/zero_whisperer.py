__author__ = 'amaury'

import zmq
import time
sock = zmq.Context.instance().socket(zmq.PUB)
sock.bind('ipc:///tmp/zerobus')

while True:
    message = sock.send("i know what you did last summer")
    time.sleep(1)
