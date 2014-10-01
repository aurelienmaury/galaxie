#! /usr/bin/python
# -*- coding: utf-8 -*-

#Instead of adding silence at start and end of recording (values=0) I add the original audio . This makes audio sound more natural as volume is >0. See trim()
#I also fixed issue with the previous code - accumulated silence counter needs to be cleared once recording is resumed.

from array import array
from struct import pack
from sys import byteorder
import copy
import pyaudio
import audioop
import wave
import commands
import sys
import commands
from os import system
import aiml
import marshal 
import os.path
import time
import tempfile
import subprocess

# Write STDERR to /dev/null
#f = open('/dev/null', 'w')
#sys.stderr = f

# VARIALE for Voice reconize
pocketsphinx_share_path = subprocess.Popen("pkg-config --variable=modeldir pocketsphinx", stdout=subprocess.PIPE, shell=True)
(pocketsphinx_share_path_output, pocket_sphinx_share_path_err) = pocketsphinx_share_path.communicate()
pocketsphinx_share_path_output = pocketsphinx_share_path_output.replace('\n', '')
print pocketsphinx_share_path_output+'/lm/fr_FR/frenchWords62K.dic'
if os.path.isfile(pocketsphinx_share_path_output+'/lm/fr_FR/frenchWords62K.dic'):
    hmdir =  pocketsphinx_share_path_output + "/hmm/fr_FR/french_f0"
    lmd = pocketsphinx_share_path_output + "/lm/fr_FR/french3g62K.lm.dmp"
    dictd = pocketsphinx_share_path_output + "/lm/fr_FR/frenchWords62K.dic"
else:
    print 'pocketsphinx is require for zoevoice'
    os.system(sys.exit(0));

# VARIABLES for Noise Gate Regarding
THRESHOLD = 2000  # audio levels not normalised.
CHUNK_SIZE = 1024
SILENT_CHUNKS = 0.3 * 44100 / 1024  # about 3sec
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-0.3 / 20)
RATE = 16000
CHANNELS = 1
TRIM_APPEND = RATE / 10
DEBUG = 1


# ALICE BRAIN INT
k = aiml.Kernel()
zoe_brain="zoe.br"
zoe_session="zoe.ses"

# read dictionary and create brain in file zoe.brp

if os.path.isfile(zoe_brain):
    k.bootstrap(brainFile = zoe_brain)
else:
    homedir=os.getcwd()
    #Change to the directory whe	re the AIML files are located
    os.chdir('./dic') # going to dictionary
    list=os.listdir('./');
    for item in list: #load dictionary one by one 
        k.learn(item)
    
    k.setPredicate("master","Zoe")
    #k.setPredicate("master","ravi")
    #k.setPredicate(pred, value, "Zoe")
	
    #Change back to homedir to save the brain for subsequent loads
    os.chdir(homedir)
    k.saveBrain(zoe_brain) # save new brain
# name of bot
k.setBotPredicate('name', "Zoe")

#Load session
if os.path.isfile(zoe_session):
    sessionFile = file(zoe_session, "rb")
    session = marshal.load(sessionFile)
    for pred,value in session.items():
        k.setPredicate(pred, value, "Zoe")


#Temporaty file
wavfile = tempfile.gettempdir() + '/zoevoice_'+str(int(time.time())) + '.wav'

#Espeack command line
#espeack_cmd = "espeak -x -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -e -C \"n n2\" -v 0.5 -f 3.0 -t 2.0 -l 16000 /usr/share/mbrola/fr4/fr4 - -.au | paplay"
#espeack_cmd = "espeak -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -e -v 0.5 -f 3.0 -t 2.0 /usr/share/mbrola/fr4/fr4 - -.au | paplay"
espeack_cmd = "espeak -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -e /usr/share/mbrola/fr4/fr4 - -.au | paplay"

#Variable it contain the text ecognised by the voice to text
global recognised

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    NORMAL = '\033[36m'
    RED =  '\033[31m'
    BLUE =  '\033[34m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.YELLOW = ''
        self.NORMAL=''
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
            prompt(2)              

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    data_all = trim(data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
    data_all = normalize(data_all)
    return sample_width, data_all

def record_to_file(path):
    #"Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)

    wave_file = wave.open(path, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(RATE)
    wave_file.writeframes(data)
    wave_file.close()

def decodeSpeech(hmmd,lmdir,dictp,wavfile):
    
    prompt(3)
 
    import pocketsphinx as ps
    import sphinxbase
    
    speechRec = ps.Decoder(hmm = hmmd, lm = lmdir, dict = dictp)
    wavFile = file(wavfile,'rb')
    wavFile.seek(44)
    speechRec.decode_raw(wavFile)
    result = speechRec.get_hyp()
    
    prompt(0)

    return result[0]

def prompt(state):
    print "\b"*20,
    if state == 1:
       print bcolors.NORMAL+"\b["+bcolors.ENDC,
       print bcolors.OKGREEN+"\bPrêt   "+bcolors.ENDC,
       print bcolors.NORMAL+"\b >"+bcolors.ENDC,
    if state == 2:
       print bcolors.NORMAL+"\b["+bcolors.ENDC,
       print bcolors.YELLOW+"\bEcoute "+bcolors.ENDC,
       print bcolors.NORMAL+"\b >"+bcolors.ENDC,
    if state == 3:
       print bcolors.NORMAL+"\b["+bcolors.ENDC,
       print bcolors.RED+"\bAnalyse"+bcolors.ENDC,
       print bcolors.NORMAL+"\b >"+bcolors.ENDC,
    sys.stdout.flush()
    
  
def tts(text):
    if not text == "": 
        print bcolors.NORMAL+"\bIA   :> "+bcolors.YELLOW+text+bcolors.ENDC
        os.system(espeack_cmd % text)

def stt():
    record_to_file(wavfile)
    recognised = decodeSpeech(hmdir,lmd,dictd,wavfile)
    os.remove(wavfile)
    if not recognised == "": 
        print bcolors.NORMAL+"\bHuman:> "+bcolors.YELLOW+recognised+bcolors.ENDC
    return recognised
    

def main():
    
    while True:
        
        prompt(1)
        
        recognised = stt()
        tts(k.respond(recognised, 'Zoe'))
        
        if recognised == "lance un navigateur" or recognised == "lance un médiateur":
            os.system("iceweasel");
            tts("C'est fait")
        elif recognised == "je vais me coucher":
            tts("OK, veux tu que je ferme tout ?")
            prompt(1)
            recognised = stt()
            if recognised == "oui":
                tts("OK, je fais ça")
                os.system("sudo /sbin/shutdown -h 0");
                os.system(sys.exit(0));
        elif recognised == "ferme":
            tts("Au revoir")
            session = k.getSessionData("Zoe")
            sessionFile = file(zoe_session, "wb")
            marshal.dump(session, sessionFile)
            sessionFile.close()
            os.system(sys.exit(0));
        elif recognised == "ferme toi":
            tts("Au revoir")
            os.system(sys.exit(0));

if __name__ == '__main__':
    main()
