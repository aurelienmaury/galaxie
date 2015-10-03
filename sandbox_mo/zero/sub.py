import zmq

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.SUB)

# Define subscription and messages with prefix to accept.
sock.setsockopt(zmq.SUBSCRIBE, "pub")
sock.connect("ipc:///tmp/zerolab")

while True:
    message= sock.recv()
    print message