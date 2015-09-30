__author__ = 'amaury'

import zmq

sock = zmq.Context.instance().socket(zmq.SUB)
sock.setsockopt(zmq.SUBSCRIBE, '')
sock.connect('ipc:///tmp/zerolab')

while True:
    message = sock.recv()
    print message.upper()