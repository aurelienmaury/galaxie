__author__ = 'tuxa@rtnp.org'

import os
import sys


class Voice(object):

    def __init__(self):
        # Espeack command line
        # self.espeack_cmd = "espeak -x -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -e -C \"n n2\" -v 0.5 -f 3.0 -t 2.0 -l 16000 /usr/share/mbrola/fr4/fr4 - -.au | paplay"
        # self.espeack_cmd = "espeak -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -e -v 0.5 -f 3.0 -t 2.0 /usr/share/mbrola/fr4/fr4 - -.au | paplay"
        # self.espeack_cmd = "espeak -s 130 -p 35 -v mb/mb-fr4 \"%s\" --pho | mbrola -e -v 0.5 -f 3.0 -t 2.0 /usr/share/mbrola/fr4/fr4 - -.au| paplay"
        # self.espeack_cmd = "espeak -v mb/mb-fr4 \"%s\" --pho | mbrola -e -v 1.0 -f 1.2 -t 1.4 -l 30000 /usr/share/mbrola/fr4/fr4 - -.au|aplay"
        # self.espeack_cmd = "espeak -v mb/mb-fr4 \"%s\" --pho | mbrola -e -f 1.5 /usr/share/mbrola/fr4/fr4 - -| aplay -r16000 -fS16 "
        # self.espeack_cmd = "echo  \"%s\" | mbrola  -t 1.2 -f 1.3  -e /usr/share/mbrola/fr4/fr4 - -.au | play -t au - pitch 200 tremolo 500 echo 0.9 0.8 33 0.9"
        self.espeack_cmd = ''
        self.espeack_cmd += self.check_espeack()
        self.espeack_cmd += ' '
        self.espeack_cmd += '-v mb/mb-fr4 -q -s150  --pho --stdout \"%s\"'
        self.espeack_cmd += ' | '
        self.espeack_cmd += self.check_mbrola()
        self.espeack_cmd += ' '
        self.espeack_cmd += '-t 1.2 -f 1.4 -e /usr/share/mbrola/fr4/fr4 - -.au'
        self.espeack_cmd += ' | '
        self.espeack_cmd += self.check_play()
        self.espeack_cmd += ' '
        self.espeack_cmd += '-t au - bass +1 pitch -300 echo 0.8 0.4 99 0.3'

    def text_to_speech(self, text):
        if not text == '':
            os.system(self.espeack_cmd % text)

    def check_espeack(self):
        if not self.get_app_path('espeak'):
            print "Error: Espeack is require, for enable voice"
            print "Error: Please install \"espeak\" or verify it is aviable on your $PATH env var"
            sys.exit(1)
        else:
            return self.get_app_path('espeak')

    def check_mbrola(self):
        if not self.get_app_path('mbrola'):
            print "Error: Mbrola is require, for enable voice"
            print "Error: Please install \"mbrola\" or verify it is aviable on your $PATH env var"
            sys.exit(1)
        else:
            return self.get_app_path('mbrola')

    def check_play(self):
        if not self.get_app_path('play'):
            print "Error: Sox tool is require, for enable voice"
            print "Error: Please install \"Sox Player\" or verify it is aviable on your $PATH env var"
            sys.exit(1)
        else:
            return self.get_app_path('play')

    def get_app_path(self, program):
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file
        return None
