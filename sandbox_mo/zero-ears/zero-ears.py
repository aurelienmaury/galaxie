#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of zero-ears.
#
# zero-ears is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# zero-ears is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with zero-ears.  If not, see <http://www.gnu.org/licenses/>.
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org>

import zmq
import copy
import wave
import time
import tempfile
import os
import sys
import pyaudio
import proc
from array import array
from struct import pack

global bus

SELF_PATH = os.path.dirname(os.path.realpath(__file__))
NOISE_THRESHOLD = 3000
READ_CHUNK_SIZE = 1024

SAMPLE_RATE = 16000
# END_OF_SPEECH_SILENCE_DURATION = 3 * SAMPLE_RATE / READ_CHUNK_SIZE
END_OF_SPEECH_SILENCE_DURATION = 0.3 * 44100 / READ_CHUNK_SIZE
MAX_FRAME = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_DB = 10 ** (-3 / 20)

NB_CHANNELS = 1
FORMAT = pyaudio.paALSA

TRIM_APPEND = SAMPLE_RATE / 10


def main():
    zmq_ctx = zmq.Context()

    publish_zmq_channel = "ipc:///tmp/zero_ears_bus"

    global bus
    bus = zmq_ctx.socket(zmq.PUB)
    bus.bind(publish_zmq_channel)

    while True:
        print "zero-ears loop"
        bus.send(">ears>state>init")

        recognizing = decode_speech(
            os.path.join(sys.argv[1], sys.argv[2]),
            os.path.join(sys.argv[1], sys.argv[2]+".lm.dmp"),
            os.path.join(sys.argv[1], sys.argv[2]+".dic")
        )

        if recognizing:
            print "zero-ears:perceive:" + recognizing
            bus.send(">ears>perceive>" + recognizing)


def is_silence(data_chunk):
    return max(data_chunk) < NOISE_THRESHOLD


def normalize(data_all):
    """ Amplify the volume out to max -1dB """
    # MAXIMUM = 16384
    normalize_factor = (float(NORMALIZE_MINUS_ONE_DB * MAX_FRAME)
                        / max(abs(i) for i in data_all))

    r = array('h')
    for i in data_all:
        r.append(int(i * normalize_factor))
    return r


def trim(data_all):
    _from = 0
    _to = len(data_all) - 1
    for i, b in enumerate(data_all):
        if abs(b) > NOISE_THRESHOLD:
            _from = max(0, i - TRIM_APPEND)
            break
    for i, b in enumerate(reversed(data_all)):
        if abs(b) > NOISE_THRESHOLD:
            _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)
            break
    return copy.deepcopy(data_all[_from:(_to + 1)])


def record():
    """Record a word or words from the microphone and
    return the data as an array of signed shorts."""

    py_audio = pyaudio.PyAudio()

    stream = py_audio.open(
        format=FORMAT,
        channels=NB_CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        output=True,
        frames_per_buffer=READ_CHUNK_SIZE
    )

    silent_chunks_counter = 0
    audio_started = False
    data_all = array('h')

    while True:
        # little endian, signed short
        data_chunk = array('h', stream.read(READ_CHUNK_SIZE))
        if sys.byteorder == 'big':
            data_chunk.byteswap()

        captured_silence = is_silence(data_chunk)
        if not captured_silence:
            data_all.extend(data_chunk)

        if audio_started:
            if captured_silence:
                silent_chunks_counter += 1
                if silent_chunks_counter > END_OF_SPEECH_SILENCE_DURATION:
                    break
            else:
                silent_chunks_counter = 0
        elif not captured_silence:
            audio_started = True
            # FIXME: replace with meaningful event
            bus.send(">ears>state>recording")

    sample_width = py_audio.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    py_audio.terminate()
    # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
    data_all = trim(data_all)
    data_all = normalize(data_all)

    return sample_width, data_all


def record_to_file(path):
    """Records from the microphone and outputs the resulting data to 'path'"""
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)
    wave_file = wave.open(path, 'wb')
    wave_file.setnchannels(NB_CHANNELS)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(SAMPLE_RATE)
    wave_file.writeframes(data)
    wave_file.close()


def decode_speech(acoustic_model_directory, language_model_file, dictionary_file):
    current_record_file = tempfile.gettempdir() + '/zero-ears_' + str(int(time.time()))
    current_record_file_wav = current_record_file + '.wav'
    current_record_file_raw = current_record_file + '.raw'

    bus.send(">ears>state>listening")
    record_to_file(current_record_file)

    status = ''
    stdout = ''
    stderr = ''

    try:
        wav_to_raw_cmd = " ".join(["sox", acoustic_model_directory, current_record_file_wav, current_record_file_raw])
        proc.run(wav_to_raw_cmd, timeout = 60)

        decoder_path = os.path.join(SELF_PATH, "pocketsphinx-head-decoder.py")
        sphinx_decode_cmd = " ".join([decoder_path, acoustic_model_directory, current_record_file_raw, " 2>/dev/null"])
        stdout, stderr, status = proc.run(sphinx_decode_cmd, timeout=10)
    except proc.Timeout:
        print "TIMED OUT: " + status + " " + stdout + " " + stderr

    print "AUDIO WAV: " + current_record_file_wav
    print "AUDIO RAW: " + current_record_file_raw
    # os.remove(current_record_file)

    return stdout.strip()


if __name__ == "__main__":
    main()
