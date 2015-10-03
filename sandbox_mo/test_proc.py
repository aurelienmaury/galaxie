#!/usr/bin/env python
# -*- coding: utf-8 -*-

import proc

stdout, stderr, exitcode = proc.run("/home/tuxa/Projets/galaxie/sandbox_mo/pocketsphinx-decoder.py /usr/share/pocketsphinx/model/hmm/fr_FR/cmusphinx /usr/share/pocketsphinx/model/lm/fr_FR/french3g62K.lm.dmp /usr/share/pocketsphinx/model/lm/fr_FR/frenchWords62K.dic /tmp/zoe_voice_1443884555.wav 2> /dev/null", timeout=2)

print "STDOUT:"+stdout