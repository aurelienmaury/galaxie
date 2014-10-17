#! /usr/bin/python
# -*- coding: utf-8 -*-

from array import array
from struct import pack
from sys import byteorder
import copy
import pyaudio
import audioop
import wave
import commands
import sys
from os import system
import aiml
import marshal 
import os.path
import time
import tempfile
import subprocess

# VARIABLES for Noise Gate Regarding
THRESHOLD = 1500  # audio levels not normalised.
CHUNK_SIZE = 1024
SILENT_CHUNKS = 0.3 * 44100 / 1024  # about 3sec
#FORMAT = pyaudio.paInt16
FORMAT = pyaudio.paALSA
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-3 / 20)
RATE = 16000
CHANNELS = 1
TRIM_APPEND = RATE / 10
DEBUG = 1

#Temporaty file
wavfile = tempfile.gettempdir() + '/zoevoice_' + str(int(time.time())) + '.wav'

# ALICE BRAIN INT
k = aiml.Kernel()
zoe_brain="zoe.br"
zoe_session="zoe.ses"
zoe_session_name="Zoe"
modules_dir= os.getcwd() + '/modules'
brains_dir= os.getcwd() + '/brains'

# VARIALE for Voice reconize
# Permit to select the right directory for model
lang='fr_FR'

#Zoevoice models dierctory, permit to difuse Zoevoie with necessary file for work out of the box
model_dir= os.getcwd() + '/model'

#Pocketsphinx directory where models are installed by default
pocketsphinx_share_path = subprocess.Popen("pkg-config --variable=modeldir pocketsphinx", stdout=subprocess.PIPE, shell=True)
(pocketsphinx_share_path_output, pocket_sphinx_share_path_err) = pocketsphinx_share_path.communicate()
pocketsphinx_share_path_output = pocketsphinx_share_path_output.replace('\n', '')

#Multilanguage support is not implemented just French yet
if lang == 'fr_FR':
    hmdir_name='lium_french_f0'
    lmd_file_name='french3g62K.lm.dmp'
    dictd_file_name='frenchWords62K.dic'
elif lang == en_UK:
    #Not implemented
    hmdir_name='lium_french_f0'
    lmd_file_name='french3g62K.lm.dmp'
    dictd_file_name='frenchWords62K.dic'

# look at that :)
local_hmdir = model_dir + '/hmm/' + lang + '/' + hmdir_name
local_lmd = model_dir + '/lm/' + lang + '/' + lmd_file_name
local_dictd = model_dir + '/lm/' + lang + '/' + dictd_file_name
pocketsphinx_hmdir = pocketsphinx_share_path_output + '/hmm/' + lang + '/' + hmdir_name
pocketsphinx_lmd = pocketsphinx_share_path_output + '/lm/' + lang + '/' + lmd_file_name
pocketsphinx_dictd = pocketsphinx_share_path_output + '/lm/' + lang + '/' + dictd_file_name

dictd = model_dir + '/lm/' + lang + '/' + dictd_file_name

# VARIALE for Voice reconize
# Load local model_dir before pocketsphinx one
if os.path.isdir(local_hmdir):
    hmdir =  local_hmdir
elif os.path.isdir(pocketsphinx_hmdir):
    hmdir = pocketsphinx_hmdir
else:
    print 'Pocketsphinx is require for Zoevoice'
    print 'Intall it properlly before use it program'
    os.system(sys.exit(0));

#Load local lm.dump before pocketsphinx one
if os.path.isfile(local_lmd):
    lmd = local_lmd
elif os.path.isfile(pocketsphinx_lmd):
    lmd = pocketsphinx_lmd
else:
    print 'A model lm.dmp is require for Zoevoice'
    print 'Put it on :' + local_lmd
    os.system(sys.exit(0));

#Load local .dic before pocketsphinx one
if os.path.isfile(local_dictd):
    dictd = local_dictd
elif os.path.isfile(pocketsphinx_dictd):
    dictd = pocketsphinx_dictd
else:
    print 'A model .dic is require for Zoevoice'
    print 'Put it on :' + local_dictd
    os.system(sys.exit(0));


#Espeack command line
#espeack_cmd = "espeak -x -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -e -C \"n n2\" -v 0.5 -f 3.0 -t 2.0 -l 16000 /usr/share/mbrola/fr4/fr4 - -.au | paplay"
#espeack_cmd = "espeak -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -e -v 0.5 -f 3.0 -t 2.0 /usr/share/mbrola/fr4/fr4 - -.au | paplay"
espeack_cmd = "espeak -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -e -C \"n n2\" -v 0.5 -f 3.0 -t 2.0 /usr/share/mbrola/fr4/fr4 - -.au | paplay"
#wavegain_cmd = "wavegain -y -d 3 \"%s\""
bassband_cmd = "sox \"%s\" \"%s\".tmp.wav sinc 200-6000"
galaxie_update_server_cmd = "xterm -hold -e /home/tuxa/ansible/bin/ansible-playbook ~/galaxie/update-server.yml -K&"

#Variable it contain the text ecognised by the voice to text
global recognised

class bcolors:
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    NORMAL = '\033[36m'
    RED =  '\033[31m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKGREEN = ''
        self.YELLOW = ''
        self.NORMAL=''
        self.RED=''
        self.ENDC = ''


def is_silent(data_chunk):
    """Returns 'True' if below the 'silent' threshold"""
    #print max(data_chunk)
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
    """Records from the microphone and outputs the resulting data to 'path'"""
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)
    wave_file = wave.open(path, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(RATE)
    wave_file.writeframes(data)
    wave_file.close()
    #filter_noise(wavfile)
    #os.system(wavegain_cmd % path)
    os.system(bassband_cmd % (wavfile,wavfile))
    os.rename(wavfile+'.tmp.wav', wavfile)
    
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
    print "\b" * 20,
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
        print bcolors.NORMAL+"\bNestor:> "+bcolors.YELLOW+text+bcolors.ENDC
        os.system(espeack_cmd % text)

def stt():
    record_to_file(wavfile)
    recognised = decodeSpeech(hmdir,lmd,dictd,wavfile)
    if not recognised == '':
        #recognised.decode('iso-8859-1').encode('utf8')
        #recognised.decode('utf8').encode('iso-8859-1')
        print bcolors.NORMAL+"\bHuman :> "+bcolors.YELLOW+recognised+bcolors.ENDC
    os.remove(wavfile)
    return recognised


def load_module(module_name):
    os.chdir(modules_dir + '/' + module_name + '/' + lang)
    list=os.listdir('./');
    for item in list:
       if item.endswith('.aiml'):
            k.learn(item)

def reload_modules():
    os.chdir(brains_dir)
    os.remove(zoe_brain)
    load_brain()
    save_session()    

def load_brain():
    """ read dictionary and create brain in file zoe.brp"""
    os.chdir(brains_dir)
    if os.path.isfile(zoe_brain):
        k.bootstrap(brainFile = zoe_brain)
    else:
        load_module('zoe')
        load_module('date')
        load_module('meteo')
        load_module('alice')
        os.chdir(brains_dir)
        k.setPredicate("master",zoe_session_name)
        k.saveBrain(zoe_brain) # save new brain
    # name of bot
    k.setBotPredicate('name', zoe_session_name)

def load_session():
    os.chdir(brains_dir)
    if os.path.isfile(zoe_session):
        sessionFile = file(zoe_session, "rb")
        session = marshal.load(sessionFile)
        for pred,value in session.items():
            k.setPredicate(pred, value, zoe_session_name)
    
def save_session():
    os.chdir(brains_dir)
    session = k.getSessionData(zoe_session_name)
    sessionFile = file(zoe_session, "wb")
    marshal.dump(session, sessionFile)
    sessionFile.close()   

def main():
    load_brain()
    load_session()
    while True:
        prompt(1)
        recognised = stt()
        tts(k.respond(recognised, zoe_session_name))
        
        if recognised == "lance un navigateur" or recognised == "lance un médiateur":
            os.system("iceweasel");
            tts("C'est fait")
        elif recognised == "mis à jour des modules" or recognised == "mise jour des modules" or recognised == "mise à jour des modules" or recognised == "mise à jour de modules":
            reload_modules()
            tts("C'est fait")
        elif recognised == "je vais me coucher":
            tts("OK, veux tu que je ferme tout ?")
            prompt(1)
            recognised = stt()
            if recognised == "oui":
                tts("OK, je fais ça")
                save_session()
                os.system("sudo /sbin/shutdown -h 0");
                os.system(sys.exit(0));
        elif recognised == "ferme" or recognised == "quitte":
            tts("Au revoir")
            save_session()
            os.system(sys.exit(0));
        elif recognised == "mise à jour des machines" or recognised == 'mais un jour les machines' or recognised == 'mais le jour les machines':
            tts("Entre ton mot de passe")
            os.system(galaxie_update_server_cmd)

if __name__ == '__main__':
    main()
