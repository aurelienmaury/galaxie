#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'amaury'

import pocketsphinx
import sys

acoustic_model_directory = sys.argv[1]
language_model_file = sys.argv[2]
dictionary_file = sys.argv[3]
wavfile = sys.argv[4]

speech_rec = pocketsphinx.Decoder(
    hmm=acoustic_model_directory,
    lm=language_model_file,
    dict=dictionary_file
)
wav_file_to_decode = file(wavfile, 'rb')
wav_file_to_decode.seek(44)
speech_rec.decode_raw(wav_file_to_decode)

result = speech_rec.get_hyp()

print result[0]
