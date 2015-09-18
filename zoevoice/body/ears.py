# -*- coding: utf-8 -*-
__author__ = 'tuxa@rtnp.org'

from array import array
from struct import pack
from sys import byteorder
import copy
import pyaudio
import wave
import time
import tempfile
import pocketsphinx
import os
import sys


class bcolors:
    green = '\033[92m'
    yellow = '\033[93m'
    normal = '\033[36m'
    red = '\033[31m'
    end = '\033[0m'

    def disable(self):
        self.green = ''
        self.yellow = ''
        self.normal = ''
        self.red = ''
        self.end = ''


def set_prompt_type(state):
    print "\b" * 20,
    if state == 1:
        print bcolors.normal + "\b[" + bcolors.end,
        print bcolors.green + "\bPrêt   " + bcolors.end,
        print bcolors.normal + "\b >" + bcolors.end,
    if state == 2:
        print bcolors.normal + "\b[" + bcolors.end,
        print bcolors.yellow + "\bEcoute " + bcolors.end,
        print bcolors.normal + "\b >" + bcolors.end,
    if state == 3:
        print bcolors.normal + "\b[" + bcolors.end,
        print bcolors.red + "\bAnalyse" + bcolors.end,
        print bcolors.normal + "\b >" + bcolors.end,
    sys.stdout.flush()


class Ears(object):

    def __init__(self):
        # VARIABLES for Noise Gate Regarding
        self.threshold = 3000  # audio levels not normalised.
        self.chunk_size = 1024
        self.silent_chunks = 0.3 * 44100 / 1024  # about 3sec
        # self.format = pyaudio.paInt16
        self.format = pyaudio.paALSA
        self.frame_max_value = 2 ** 15 - 1
        self.normalize_minus_one_db = 10 ** (-3 / 20)
        self.rate = 16000
        self.channels = 1
        self.trim_append = self.rate / 10
        # Temporary file
        self.wavfile = tempfile.gettempdir() + '/zoe_voice_' + str(int(time.time())) + '.wav'
        self.lang = 'fr_FR'
        self.pocket_sphinx_share_path_output = "/usr/share/pocketsphinx/model"
        # Multilanguage support is not implemented just French yet
        if self.lang == 'fr_FR':
            self.hmdir_name = 'cmusphinx'
            self.lmd_file_name = 'french3g62K.lm.dmp'
            self.dict_file_name = 'frenchWords62K.dic'
        self.acoustic_model_directory = self.pocket_sphinx_share_path_output + '/hmm/' + self.lang + '/' + self.hmdir_name
        self.language_model_file = self.pocket_sphinx_share_path_output + '/lm/' + self.lang + '/' + self.lmd_file_name
        self.dictionary_file = self.pocket_sphinx_share_path_output + '/lm/' + self.lang + '/' + self.dict_file_name

        if not os.path.isdir(self.acoustic_model_directory):
            print 'Pocketsphinx is require for Ears'
            print 'Intall it properlly before use it program'
            os.system(sys.exit(0))

        # Load local lm.dump before pocketsphinx one
        if not os.path.isfile(self.language_model_file):
            print 'A language model file lm.dmp is require for Ears'
            print 'Put it on :' + self.language_model_file
            os.system(sys.exit(0))

        # Load local .dic before pocketsphinx one
        if not os.path.isfile(self.dictionary_file):
            print 'A dictionary .dic is require for Ears'
            print 'Put it on :' + self.dictionary_file
            os.system(sys.exit(0))

    def is_silent(self, data_chunk):
        """Returns 'True' if below the 'silent' threshold"""
        # print max(data_chunk)
        return max(data_chunk) < self.threshold

    def normalize(self, data_all):
        """Amplify the volume out to max -1dB"""
        # MAXIMUM = 16384
        normalize_factor = (float(self.normalize_minus_one_db * self.frame_max_value)
                            / max(abs(i) for i in data_all))

        r = array('h')
        for i in data_all:
            r.append(int(i * normalize_factor))
        return r

    def trim(self, data_all):
        _from = 0
        _to = len(data_all) - 1
        for i, b in enumerate(data_all):
            if abs(b) > self.threshold:
                _from = max(0, i - self.trim_append)
                break
        for i, b in enumerate(reversed(data_all)):
            if abs(b) > self.threshold:
                _to = min(len(data_all) - 1, len(data_all) - 1 - i + self.trim_append)
                break
        return copy.deepcopy(data_all[_from:(_to + 1)])

    def record(self):
        """Record a word or words from the microphone and
        return the data as an array of signed shorts."""
        p = pyaudio.PyAudio()
        stream = p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            output=True,
            frames_per_buffer=self.chunk_size
        )
        silent_chunks_counter = 0
        audio_started = False
        data_all = array('h')
        while True:
            # little endian, signed short
            data_chunk = array('h', stream.read(self.chunk_size))
            if byteorder == 'big':
                data_chunk.byteswap()
            data_all.extend(data_chunk)
            silent = self.is_silent(data_chunk)
            if audio_started:
                if silent:
                    silent_chunks_counter += 1
                    if silent_chunks_counter > self.silent_chunks:
                        break
                else:
                    silent_chunks_counter = 0
            elif not silent:
                audio_started = True
                set_prompt_type(2)
        sample_width = p.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        p.terminate()
        data_all = self.trim(
            data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
        data_all = self.normalize(data_all)
        return sample_width, data_all

    def record_to_file(self, path):
        """Records from the microphone and outputs the resulting data to 'path'"""
        sample_width, data = self.record()
        data = pack('<' + ('h' * len(data)), *data)
        wave_file = wave.open(path, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(sample_width)
        wave_file.setframerate(self.rate)
        wave_file.writeframes(data)
        wave_file.close()

    def decode_speech(self, acoustic_model_directory, language_model_file, dictionary_file, wavfile):
        set_prompt_type(3)
        speech_rec = pocketsphinx.Decoder(
            hmm=acoustic_model_directory,
            lm=language_model_file,
            dict=dictionary_file
        )
        wav_file_to_decode = file(wavfile, 'rb')
        wav_file_to_decode.seek(44)
        speech_rec.decode_raw(wav_file_to_decode)
        result = speech_rec.get_hyp()
        set_prompt_type(0)
        return result[0]