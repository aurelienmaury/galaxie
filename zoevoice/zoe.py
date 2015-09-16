#! /usr/bin/python
# -*- coding: utf-8 -*-

from array import array
from struct import pack
from sys import byteorder
import copy
import pyaudio
import wave
import sys
import aiml
import marshal
import os.path
import time
import tempfile
import pocketsphinx
import signal

playbook_directory = "/home/tuxa/Projets/galaxie/playbooks"
host_inventory_path = "/home/tuxa/Projets/galaxie/host.inventory"

# VARIABLES for Noise Gate Regarding
threshold = 3000  # audio levels not normalised.
chunk_size = 1024
silent_chunks = 0.3 * 44100 / 1024  # about 3sec
# FORMAT = pyaudio.paInt16
format = pyaudio.paALSA
frame_max_value = 2 ** 15 - 1
normalize_minus_one_db = 10 ** (-3 / 20)
rate = 16000
channels = 1
trim_append = rate / 10
debug = 1

# Temporary file
wavfile = tempfile.gettempdir() + '/zoe_voice_' + str(int(time.time())) + '.wav'

# ALICE BRAIN INT
k = aiml.Kernel()
zoe_brain = "zoe.br"
zoe_session = "zoe.ses"
zoe_session_name = "Alice"

modules_dir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "modules")
)

brains_dir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "brains")
)


# Permit to select the right directory for model
lang = 'fr_FR'

# Zoevoice models dierctory, permit to difuse Zoevoie with necessary file for work out of the box
model_dir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "model")
)


# Pocketsphinx directory where models are installed by default
# pocketsphinx_share_path = subprocess.Popen("pkg-config --variable=modeldir pocketsphinx", stdout=subprocess.PIPE, shell=True)
# (pocketsphinx_share_path_output, pocket_sphinx_share_path_err) = pocketsphinx_share_path.communicate()
# pocketsphinx_share_path_output = pocketsphinx_share_path_output.replace('\n', '')
pocket_sphinx_share_path_output = "/usr/share/pocketsphinx/model"
# Multilanguage support is not implemented just French yet
if lang == 'fr_FR':
    hmdir_name = 'cmusphinx'
    lmd_file_name = 'french3g62K.lm.dmp'
    dict_file_name = 'frenchWords62K.dic'
elif lang == 'en_UK':
    # Not implemented
    hmdir_name = 'lium_french_f0'
    lmd_file_name = 'french3g62K.lm.dmp'
    dict_file_name = 'frenchWords62K.dic'

# look at that :)
local_hm_directory = model_dir + '/hmm/' + lang + '/' + hmdir_name
local_lmd = model_dir + '/lm/' + lang + '/' + lmd_file_name
local_dictd = model_dir + '/lm/' + lang + '/' + dict_file_name
pocket_sphinx_hm_directory = pocket_sphinx_share_path_output + '/hmm/' + lang + '/' + hmdir_name
pocket_sphinx_lmd = pocket_sphinx_share_path_output + '/lm/' + lang + '/' + lmd_file_name
pocket_sphinx_dictd = model_dir + '/lm/' + lang + '/' + dict_file_name

dictionary_file = model_dir + '/lm/' + lang + '/' + dict_file_name

# VARIALE for Voice reconize
# Load local model_dir before pocketsphinx one
if os.path.isdir(local_hm_directory):
    acoustic_model_directory = local_hm_directory
elif os.path.isdir(pocket_sphinx_hm_directory):
    acoustic_model_directory = pocket_sphinx_hm_directory
else:
    print 'Pocketsphinx is require for Zoevoice'
    print 'Intall it properlly before use it program'
    os.system(sys.exit(0))

# Load local lm.dump before pocketsphinx one
if os.path.isfile(local_lmd):
    language_model_file = local_lmd
elif os.path.isfile(pocket_sphinx_lmd):
    language_model_file = pocket_sphinx_lmd
else:
    print 'A model lm.dmp is require for Zoevoice'
    print 'Put it on :' + local_lmd
    os.system(sys.exit(0))

# Load local .dic before pocketsphinx one
if os.path.isfile(local_dictd):
    dictionary_file = local_dictd
elif os.path.isfile(pocket_sphinx_dictd):
    dictionary_file = pocket_sphinx_dictd
else:
    print 'A model .dic is require for Zoevoice'
    print 'Put it on :' + local_dictd
    os.system(sys.exit(0))


# Espeack command line
# espeack_cmd = "espeak -x -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -e -C \"n n2\" -v 0.5 -f 3.0 -t 2.0 -l 16000 /usr/share/mbrola/fr4/fr4 - -.au | paplay"
# espeack_cmd = "espeak -s 130 -p 35 -v mb/mb-fr4 \"%s\" | mbrola -e -v 0.5 -f 3.0 -t 2.0 /usr/share/mbrola/fr4/fr4 - -.au | paplay"
# espeack_cmd = "espeak -s 130 -p 35 -v mb/mb-fr4 \"%s\" --pho | mbrola -e -v 0.5 -f 3.0 -t 2.0 /usr/share/mbrola/fr4/fr4 - -.au| paplay"
# espeack_cmd = "espeak -v mb/mb-fr4 \"%s\" --pho | mbrola -e -v 1.0 -f 1.2 -t 1.4 -l 30000 /usr/share/mbrola/fr4/fr4 - -.au|aplay"
# espeack_cmd = "espeak -v mb/mb-fr4 \"%s\" --pho | mbrola -e -f 1.5 /usr/share/mbrola/fr4/fr4 - -| aplay -r16000 -fS16 "
# espeack_cmd = "echo  \"%s\" | mbrola  -t 1.2 -f 1.3  -e /usr/share/mbrola/fr4/fr4 - -.au | play -t au - pitch 200 tremolo 500 echo 0.9 0.8 33 0.9"
espeack_cmd = "espeak -v mb/mb-fr4 -q -s150  --pho --stdout \"%s\" | " \
              "mbrola -t 1.2 -f 1.4 -e /usr/share/mbrola/fr4/fr4 - -.au | " \
              "play -t au - bass +1 pitch -300 echo 0.8 0.4 99 0.3"

# espeack_cmd = "espeak -v mb/mb-fr4 -q -s150  --pho  \"%s\" | mbrola  -t 1.2 -f 1.3  -e /usr/share/mbrola/fr4/fr4 - -.au | play -t au - pitch -200 echo 0.9 0.8 33 0.9"
# wavegain_cmd = "wavegain -y -d 3 \"%s\""
bassband_cmd = "sox \"%s\" \"%s\".tmp.wav sinc 100-8000"
galaxie_update_hosts_cmd = "gnome-terminal.wrapper -hold -e ansible-playbook -i " + \
                           host_inventory_path + " " + playbook_directory + "/galaxie-upgrade.yml"

# Variable it contain the text ecognised by the voice to text
global recognised


class bcolors:
    ok_green = '\033[92m'
    yellow = '\033[93m'
    normal = '\033[36m'
    red = '\033[31m'
    endc = '\033[0m'

    def disable(self):
        self.ok_green = ''
        self.yellow = ''
        self.normal = ''
        self.red = ''
        self.endc = ''


def is_silent(data_chunk):
    """Returns 'True' if below the 'silent' threshold"""
    # print max(data_chunk)
    return max(data_chunk) < threshold


def normalize(data_all):
    """Amplify the volume out to max -1dB"""
    # MAXIMUM = 16384
    normalize_factor = (float(normalize_minus_one_db * frame_max_value)
                        / max(abs(i) for i in data_all))

    r = array('h')
    for i in data_all:
        r.append(int(i * normalize_factor))
    return r


def trim(data_all):
    _from = 0
    _to = len(data_all) - 1
    for i, b in enumerate(data_all):
        if abs(b) > threshold:
            _from = max(0, i - trim_append)
            break
    for i, b in enumerate(reversed(data_all)):
        if abs(b) > threshold:
            _to = min(len(data_all) - 1, len(data_all) - 1 - i + trim_append)
            break
    return copy.deepcopy(data_all[_from:(_to + 1)])


def record():
    """Record a word or words from the microphone and 
    return the data as an array of signed shorts."""
    p = pyaudio.PyAudio()
    stream = p.open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        output=True,
        frames_per_buffer=chunk_size
    )
    silent_chunks_counter = 0
    audio_started = False
    data_all = array('h')
    while True:
        # little endian, signed short
        data_chunk = array('h', stream.read(chunk_size))
        if byteorder == 'big':
            data_chunk.byteswap()
        data_all.extend(data_chunk)
        silent = is_silent(data_chunk)
        if audio_started:
            if silent:
                silent_chunks_counter += 1
                if silent_chunks_counter > silent_chunks:
                    break
            else:
                silent_chunks_counter = 0
        elif not silent:
            audio_started = True
            set_prompt_type(2)
    sample_width = p.get_sample_size(format)
    stream.stop_stream()
    stream.close()
    p.terminate()
    data_all = trim(
        data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
    data_all = normalize(data_all)
    return sample_width, data_all


def record_to_file(path):
    """Records from the microphone and outputs the resulting data to 'path'"""
    sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)
    wave_file = wave.open(path, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(sample_width)
    wave_file.setframerate(rate)
    wave_file.writeframes(data)
    wave_file.close()

    # Few test abut Effect before other post processing
    # filter_noise(wavfile)
    # os.system(wavegain_cmd % path)
    # os.system(bassband_cmd % (path, path))
    # os.rename(path + '.tmp.wav', path)


def decode_speech(acoustic_model_directory, language_model_file, dictionary_file, wavfile):
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


def set_prompt_type(state):
    print "\b" * 20,
    if state == 1:
        print bcolors.normal + "\b[" + bcolors.endc,
        print bcolors.ok_green + "\bPrêt   " + bcolors.endc,
        print bcolors.normal + "\b >" + bcolors.endc,
    if state == 2:
        print bcolors.normal + "\b[" + bcolors.endc,
        print bcolors.yellow + "\bEcoute " + bcolors.endc,
        print bcolors.normal + "\b >" + bcolors.endc,
    if state == 3:
        print bcolors.normal + "\b[" + bcolors.endc,
        print bcolors.red + "\bAnalyse" + bcolors.endc,
        print bcolors.normal + "\b >" + bcolors.endc,
    sys.stdout.flush()


def tts(text):
    if not text == "":
        print "{0}\b{4} :> {1}{2}{3}".format(bcolors.normal, bcolors.yellow, text, bcolors.endc, zoe_session_name)
        os.system(espeack_cmd % text)


def stt():
    record_to_file(wavfile)
    recognizing = decode_speech(
        acoustic_model_directory,
        language_model_file,
        dictionary_file,
        wavfile
    )
    if not recognizing == '':
        # recognizing.decode('iso-8859-1').encode('utf8')
        # recognizing.decode('utf8').encode('iso-8859-1')
        print bcolors.normal + "\bHuman :> " + bcolors.yellow + recognizing + bcolors.endc
    os.remove(wavfile)
    return recognizing


def load_module(module_name):
    path = modules_dir + '/' + module_name + '/' + lang
    # print path
    os.chdir(path)
    list_files = os.listdir("./")
    for item in list_files:
        if item.endswith('.aiml'):
            k.learn(os.path.join(path, item))


def reload_modules():
    os.chdir(brains_dir)
    os.remove(zoe_brain)
    load_brain()
    save_session()


def load_brain():
    """ read dictionary and create brain in file zoe.brp"""
    os.chdir(brains_dir)
    if os.path.isfile(zoe_brain):
        k.bootstrap(brainFile=zoe_brain)
    else:
        load_module('zoe')
        load_module('date')
        load_module('meteo')
        load_module('desktop')
        load_module('ansible')
        # load_module('alice')
        os.chdir(brains_dir)
        k.setPredicate("master", zoe_session_name)
        k.saveBrain(zoe_brain)  # save new brain
    # name of bot
    k.setBotPredicate('name', zoe_session_name)


def load_session():
    os.chdir(brains_dir)
    if os.path.isfile(zoe_session):
        sessionFile = file(zoe_session, "rb")
        session = marshal.load(sessionFile)
        for pred, value in session.items():
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
    reload_modules_text = [
        "mis à jour des modules",
        "mis à jour les modules",
        "mise jour des modules",
        "mise à jour des modules",
        "mise à jour les modules",
        "mais un jour les modules",
        "mais un jour des modules",
        "mais le jour les modules",
        "mais à ce jour les modules",
        "recharger modules",
        "recharger les modules",
        "en charge des modules",
        "charges les modules",
        "recherché modules",
        "mais sur les modules",
        "rogers les modules",
        "on recharge les modules",
        "recherche module",
        "recherche les modules",
        "bien_sûr les modules",
        "mais sur les modes",
        "modules reload"
    ]

    upgrade_text = [
        "mis à jour les machines",
        "mise à jour les machines",
        "mis à jour des machines",
        "mise à jour des machines",
        "mais un jour les machines",
        "mais un jour des machines",
        "mais le jour les machines",
        "mais à ce jour les machines",
        "mais le jour des machines"
    ]

    exit_text = [
        "ferme",
        "tu devrais fermée",
        "tu devrais fermé",
        "il devrait fermer",
        "elle devrait fermer",
        "devrait fermer",
        "quasi quitte",
        "quitte",
        "tu devrais quitter",
        "il devrait quitter",
        "elle devrait quitter",
        "qui est"
    ]
    while True:
        set_prompt_type(1)

        recognised = stt()

        tts(k.respond(recognised, zoe_session_name))

        if recognised in reload_modules_text:
            reload_modules()
            tts("C'est fait")
        elif recognised == "je vais me coucher":
            tts("OK, veux tu que je ferme tout ?")
            set_prompt_type(1)
            recognised = stt()
            if recognised == "oui":
                tts("OK, je fais ça")
                save_session()
                os.system("sudo /sbin/shutdown -h 0");
                os.system(sys.exit(0));
        elif recognised in exit_text:
            tts("Au revoir")
            save_session()
            os.system(sys.exit(0));
            # elif recognised in upgrade_text:
            #     os.system(galaxie_update_hosts_cmd)
            #     tts("Je lance ça")


if __name__ == '__main__':
    main()
