#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'

from array import array
from struct import pack

import copy
import wave
import time
import tempfile
import os
import sys
import pyaudio
import proc

# Noise gate
NOISE_THRESHOLD = 3000
READ_CHUNK_SIZE = 1024

SAMPLE_RATE = 16000
# END_OF_SPEECH_SILENCE_DURATION = 3 * SAMPLE_RATE / READ_CHUNK_SIZE
END_OF_SPEECH_SILENCE_DURATION = 0.3 * 44100 / READ_CHUNK_SIZE
MAX_FRAME = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_DB = 10 ** (-3 / 20)

NB_CHANNELS = 1
FORMAT = pyaudio.paALSA

class Ears(object):

    def __init__(self, bus):
        self.bus = bus

        self.trim_append = SAMPLE_RATE / 10
        # Temporary file
        self.wavfile = tempfile.gettempdir() + '/zoe_voice_' + str(int(time.time())) + '.wav'
        self.lang = 'fr_FR'
#        self.pocket_sphinx_share_path_output = "/usr/share/pocketsphinx/model"
        self.pocket_sphinx_share_path_output = "/usr/local/Cellar/cmu-pocketsphinx/0.8/share/pocketsphinx/model"

        # Multilanguage support is not implemented just French yet
        if self.lang == 'fr_FR':
            self.hmdir_name = 'cmusphinx'
            self.lmd_file_name = 'french3g62K.lm.dmp'
            self.dict_file_name = 'frenchWords62K.dic'

        self.acoustic_model_directory = self.pocket_sphinx_share_path_output + '/hmm/' + self.lang + '/' + self.hmdir_name
        self.language_model_file = self.pocket_sphinx_share_path_output + '/lm/' + self.lang + '/' + self.lmd_file_name
        self.dictionary_file = self.pocket_sphinx_share_path_output + '/lm/' + self.lang + '/' + self.dict_file_name

    def is_silence(self, data_chunk):
        return max(data_chunk) < NOISE_THRESHOLD

    def normalize(self, data_all):
        """ Amplify the volume out to max -1dB """
        # MAXIMUM = 16384
        normalize_factor = (float(NORMALIZE_MINUS_ONE_DB * MAX_FRAME)
                            / max(abs(i) for i in data_all))

        r = array('h')
        for i in data_all:
            r.append(int(i * normalize_factor))
        return r

    def trim(self, data_all):
        _from = 0
        _to = len(data_all) - 1
        for i, b in enumerate(data_all):
            if abs(b) > NOISE_THRESHOLD:
                _from = max(0, i - self.trim_append)
                break
        for i, b in enumerate(reversed(data_all)):
            if abs(b) > NOISE_THRESHOLD:
                _to = min(len(data_all) - 1, len(data_all) - 1 - i + self.trim_append)
                break
        return copy.deepcopy(data_all[_from:(_to + 1)])

    def record(self):
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

            captured_silence = self.is_silence(data_chunk)
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
                self.bus.send(">ears>PROMPT TYPE 2")

        sample_width = py_audio.get_sample_size(FORMAT)
        stream.stop_stream()
        stream.close()
        py_audio.terminate()
        # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
        data_all = self.trim(data_all)
        data_all = self.normalize(data_all)
        return sample_width, data_all

    def record_to_file(self, path):
        """Records from the microphone and outputs the resulting data to 'path'"""
        sample_width, data = self.record()
        data = pack('<' + ('h' * len(data)), *data)
        wave_file = wave.open(path, 'wb')
        wave_file.setnchannels(NB_CHANNELS)
        wave_file.setsampwidth(sample_width)
        wave_file.setframerate(SAMPLE_RATE)
        wave_file.writeframes(data)
        wave_file.close()

    def decode_speech(self, acoustic_model_directory, language_model_file, dictionary_file, wavfile):

        self.record_to_file(self.wavfile)

        # FIXME: replace with meaningful event
        self.bus.send(">ears>PROMPT TYPE 3")

        try:
            status = ''
            stdout = ''
            stderr = ''

            try:
                last_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pocketsphinx-head-decoder.py")
                stdout, stderr, status = proc.run(last_path+" "+os.path.dirname(os.path.realpath(__file__))+"/../../audition-mo/ "+wavfile+" 2>/dev/null", timeout=60)
            except proc.Timeout:
                print "TIMED OUT: "+status+" "+stdout+" "+stderr

            print "WAV: "+self.wavfile
            #os.remove(self.wavfile)

            return stdout.strip()

        except KeyboardInterrupt:
            sys.exit(0)
