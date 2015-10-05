#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'amaury'

import sys
from os import path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = sys.argv[1]

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'fr-fr/fr-fr'))
config.set_string('-lm', path.join(MODELDIR, 'fr-fr/fr-fr.lm.dmp'))
config.set_string('-dict', path.join(MODELDIR, 'fr-fr/cmudict-fr-fr.dict'))
decoder = Decoder(config)

wavfile = sys.argv[2]

decoder.start_utt()
stream = open(wavfile, 'rb')

while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
    else:
        break

decoder.end_utt()

print decoder.hyp().hypstr