__author__ = 'amaury'

import zmq
import time
import os
from ears import Ears

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.PUB)
sock.bind("ipc:///tmp/little_alice_ears")

ears = Ears()

while True:
    ears.record_to_file(ears.wavfile)

    recognizing = ears.decode_speech(
        ears.acoustic_model_directory,
        ears.language_model_file,
        ears.dictionary_file,
        ears.wavfile
    )

    sock.send("ears:" + time.ctime() + ":" + recognizing)

    os.remove(ears.wavfile)
