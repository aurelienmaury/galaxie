#! /usr/bin/python
# -*- coding: utf-8 -*-

#Instead of adding silence at start and end of recording (values=0) I add the original audio . This makes audio sound more natural as volume is >0. See trim()
#I also fixed issue with the previous code - accumulated silence counter needs to be cleared once recording is resumed.

from array import array
from struct import pack
from sys import byteorder
import copy
import pyaudio
import wave
import aiml
import commands
import sys
import time 
import commands
from os import system
import marshal # sesje 
import os.path

hmdir = "/usr/share/pocketsphinx/model/hmm/fr_FR/french_f0"
lmd = "/usr/share/pocketsphinx/model/lm/fr_FR/french3g62K.lm.dmp"
dictd = "/usr/share/pocketsphinx/model/lm/fr_FR/frenchWords62K.dic"

THRESHOLD = 1500  # audio levels not normalised.
CHUNK_SIZE = 1024
SILENT_CHUNKS = 0.1 * 44100 / 1024  # about 3sec
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-0.5 / 20)
RATE = 16000
CHANNELS = 1
TRIM_APPEND = RATE / 4
DEBUG = 1


k = aiml.Kernel()
zoe="zoe.br"

# read dictionary and create brain in file zoe.brp

if os.path.isfile(zoe):
    k.bootstrap(brainFile = zoe)
else:
    homedir=os.getcwd()
    #Change to the directory whe	re the AIML files are located
    os.chdir('./dic') # going to dictionary
    list=os.listdir('./');
    for item in list: #load dictionary one by one 
        k.learn(item)
	  
    
    k.setPredicate("master","ravi")
	
    #Change back to homedir to save the brain for subsequent loads
    os.chdir(homedir)
    k.saveBrain(zoe) # save new brain
# name of bot
k.setBotPredicate('name', "Zoet")


wavfile = "recording.wav"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    BLACK = '\033[36m'
    RED =  '\033[31m'
    GREEN =  '\033[32m'
    BLUE =  '\033[34m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.BLACK=''
        self.RED=''
        self.FAIL = ''
        self.ENDC = ''


def is_silent(data_chunk):
    """Returns 'True' if below the 'silent' threshold"""
    return max(data_chunk) < THRESHOLD

def normalize(data_all):
    """Amplify the volume out to max -1dB"""
    # MAXIMUM = 16384
    normalize_factor = (float(NORMALIZE_MINUS_ONE_dB * FRAME_MAX_VALUE)
                        / max(abs(i) for i in data_all))

    r = array('h')
    for i in data_all:
        r.append(int(i * normalize_factor))
    return r

def trim(data_all):
    _from = 0
    _to = len(data_all) - 1
    for i, b in enumerate(data_all):
        if abs(b) > THRESHOLD:
            _from = max(0, i - TRIM_APPEND)
            break

    for i, b in enumerate(reversed(data_all)):
        if abs(b) > THRESHOLD:
            _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)
            break

    return copy.deepcopy(data_all[_from:(_to + 1)])

def record():
    """Record a word or words from the microphone and 
    return the data as an array of signed shorts."""

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

    silent_chunks = 0
    audio_started = False
    data_all = array('h')
    while True:
        # little endian, signed short
        data_chunk = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            data_chunk.byteswap()
        data_all.extend(data_chunk)

        silent = is_silent(data_chunk)

        if audio_started:
            if silent:
                silent_chunks += 1
                if silent_chunks > SILENT_CHUNKS:
                    break
            else: 
                silent_chunks = 0
        elif not silent:
            audio_started = True              
            if DEBUG:
                print "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b",
                print bcolors.BLACK+"\b["+bcolors.ENDC,
                print bcolors.WARNING+" Ecoute  "+bcolors.ENDC,
                print bcolors.BLACK+"]"+bcolors.ENDC,
                sys.stdout.flush()

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    data_all = trim(data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
    data_all = normalize(data_all)
    return sample_width, data_all

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)

    wave_file = wave.open(path, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(RATE)
    wave_file.writeframes(data)
    wave_file.close()

def decodeSpeech(hmmd,lmdir,dictp,wavfile):
    
    print "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b",
    print bcolors.BLACK+"\b["+bcolors.ENDC,
    print bcolors.RED+" Analyse "+bcolors.ENDC,
    print bcolors.BLACK+"]"+bcolors.ENDC,
    sys.stdout.flush()
    
    import pocketsphinx as ps
    import sphinxbase
    
    speechRec = ps.Decoder(hmm = hmmd, lm = lmdir, dict = dictp)
    wavFile = file(wavfile,'rb')
    wavFile.seek(44)
    speechRec.decode_raw(wavFile)
    result = speechRec.get_hyp()
    print "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b",
    sys.stdout.flush()

    return result[0]

def tts(text):
    if not text == "": 
        print bcolors.BLACK+"\bIA   :> "+bcolors.WARNING+text+bcolors.ENDC
        os.system(espeack_cmd % text)

def stt():
    record_to_file(wavfile)
    recognised = decodeSpeech(hmdir,lmd,dictd,wavfile)
    if not recognised == "": 
        print bcolors.BLACK+"\bHuman:> "+bcolors.WARNING+recognised+bcolors.ENDC
    return recognised

if __name__ == '__main__':
    espeack_cmd = "espeak -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -v 0.5 -f 3.0 -t 2.0 -l 16000 /usr/share/mbrola/fr4/fr4 - -.au | paplay"
    while True:
        
        print "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b",
        print bcolors.BLACK+"\b["+bcolors.ENDC,
        print bcolors.OKGREEN+"Prêt    "+bcolors.ENDC,
        print bcolors.BLACK+"]"+bcolors.ENDC,
        sys.stdout.flush()
        
        recognised = stt()
        tts(k.respond(recognised))
        
        if recognised == "lance un navigateur" or recognised == "lance un médiateur":
            os.system("iceweasel");
            tts("C'est fait")
        elif recognised == "comment vas -tu" or recognised == "comment veux -tu" or recognised == "comment va" or recognised == "comment veux" or recognised == "comment ça va":
            tts("Bien merci")
            tts("Et toi ?")
            recognised = stt()
            if recognised == "mal" or recognised == "non":
                tts("Ha ?")      
        elif recognised == "je vais me coucher":
            tts("OK, veux tu que je ferme tout ?")
            recognised = stt()
            if recognised == "oui":
                tts("OK, je fais ça")
                os.system("sudo /sbin/shutdown -h 0");
                os.system(sys.exit(0));
        elif recognised == "ferme":
            tts("Au revoir")
            os.system(sys.exit(0));
        elif recognised == "ferme toi":
            tts("Au revoir")
            os.system(sys.exit(0));
