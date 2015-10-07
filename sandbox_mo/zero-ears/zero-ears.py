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
# Author: Aurélien MAURY alias "Mo" <mo@rtnp.org>

import argparse
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
NOISE_THRESHOLD = 2000
READ_CHUNK_SIZE = 1024

SAMPLE_RATE = 16000
# END_OF_SPEECH_SILENCE_DURATION = 3 * SAMPLE_RATE / READ_CHUNK_SIZE
END_OF_SPEECH_SILENCE_DURATION = 0.5 * 44100 / READ_CHUNK_SIZE
MAX_FRAME = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_DB = 10 ** (-3 / 20)

NB_CHANNELS = 1
FORMAT = pyaudio.paALSA

TRIM_APPEND = SAMPLE_RATE / 10

ZMQ_PUB_CHANNEL = "ipc:///tmp/zero_ears_bus"


def training_loop(args, loop_count):
    print "zero-ears loop:training"

    current_record_file = '/tmp/training_' + str(loop_count) + '.wav'

    decode_speech(
        os.path.join(args.acoustic_model_directory, args.acoustic_model_name),
        os.path.join(args.acoustic_model_directory, args.acoustic_model_name + ".lm.dmp"),
        os.path.join(args.acoustic_model_directory, args.acoustic_model_name + ".dic"),
        current_record_file
    )


def listen_loop(args):
    print "zero-ears loop:listen"
    bus.send(">ears>state>init")

    recognizing = decode_speech_tmp(
        os.path.join(args.acoustic_model_directory, args.acoustic_model_name),
        os.path.join(args.acoustic_model_directory, args.acoustic_model_name + ".lm.dmp"),
        os.path.join(args.acoustic_model_directory, args.acoustic_model_name + ".dic")
    )

    if recognizing:
        print "zero-ears:perceive:" + recognizing
        bus.send(">ears>perceive>" + recognizing)


def main():
    try:
        zmq_ctx = zmq.Context()

        args = parse_cli()
        global bus
        bus = zmq_ctx.socket(zmq.PUB)
        bus.bind(ZMQ_PUB_CHANNEL)

        loop_count = 0
        while True:
            if args.training:
                training_loop(args, loop_count)
            else:
                listen_loop(args)
            loop_count += 1
    except KeyboardInterrupt:
        pass


def parse_cli():
    parser = argparse.ArgumentParser(description='zero-ears')

    parser.add_argument('-m',
                        dest="acoustic_model_directory", metavar='PATH', type=str,
                        help='acoustic model directory', required=True)

    parser.add_argument('-n',
                        dest="acoustic_model_name", metavar="NAME", type=str,
                        help='acoustic model name', required=True)

    parser.add_argument('--training', action='store_true', default=False, help='sets training mode on')

    return parser.parse_args()


def get_normalize_factor(raw_audio_data):
    return float(NORMALIZE_MINUS_ONE_DB * MAX_FRAME) / max(abs(i) for i in raw_audio_data)


def normalize(raw_audio_data):
    """ Amplify the volume out to max -1dB """
    norm_factor = get_normalize_factor(raw_audio_data)

    r = array('h')
    for i in raw_audio_data:
        r.append(int(i * norm_factor))

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

        chunk_is_noisy = max(data_chunk) >= NOISE_THRESHOLD

        if audio_started or chunk_is_noisy:
            data_all.extend(data_chunk)
            if not audio_started:
                audio_started = True
                bus.send(">ears>state>recording")

        if audio_started:
            if chunk_is_noisy:
                silent_chunks_counter = 0
            else:
                silent_chunks_counter += 1
                if silent_chunks_counter > END_OF_SPEECH_SILENCE_DURATION:
                    break

    sample_width = py_audio.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    py_audio.terminate()

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


def decode_speech_tmp(acoustic_model_directory, language_model_file, dictionary_file):
    current_record_file = tempfile.gettempdir() + '/zero-ears_' + str(int(time.time())) + '.wav'
    return decode_speech(acoustic_model_directory, language_model_file, dictionary_file, current_record_file)


def decode_speech(acoustic_model_directory, language_model_file, dictionary_file, record_file):
    bus.send(">ears>state>listening")
    record_to_file(record_file)

    status = ''
    stdout = ''
    stderr = ''

    try:
        decoder_path = os.path.join(SELF_PATH, "pocketsphinx-head-decoder.py")

        sphinx_decode_cmd = " ".join([
            decoder_path,
            acoustic_model_directory,
            language_model_file,
            dictionary_file,
            record_file,
            " 2>/dev/null"
        ])
        stdout, stderr, status = proc.run(sphinx_decode_cmd, timeout=10)
    except proc.Timeout:
        print "TIMED OUT: " + status + " " + stdout + " " + stderr

    print "AUDIO WAV: " + record_file
    # os.remove(current_record_file_wav)

    return stdout.strip()


if __name__ == "__main__":
    main()
