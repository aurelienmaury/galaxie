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
