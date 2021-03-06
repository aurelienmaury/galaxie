#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'

import sys
import os.path
from body.brain import Brain
from body.voice import Voice
from body.ears import Ears
from body.eyes import Eyes
import cv2
import time
from multiprocessing import Process, Queue, TimeoutError

playbook_directory = "/home/tuxa/Projets/galaxie/playbooks"
host_inventory_path = "/home/tuxa/Projets/galaxie/host.inventory"

modules_dir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "modules")
)

brains_dir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "brains")
)

# Init Brain and kernel for the first time
brain = Brain(modules_dir, brains_dir)

# Init Voice for the first time
voice = Voice()

# Init Ears for the first time
ears = Ears()

# Init Eyes for the first time
eyes = Eyes()

# Variable it contain the text recognised by the voice to text
recognised = ''


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
        print bcolors.yellow + "\bÉcoute " + bcolors.end,
        print bcolors.normal + "\b >" + bcolors.end,
    if state == 3:
        print bcolors.normal + "\b[" + bcolors.end,
        print bcolors.red + "\bAnalyse" + bcolors.end,
        print bcolors.normal + "\b >" + bcolors.end,
    sys.stdout.flush()


def text_to_speech(text):
    if not text == "":
        print "{0}\b{4} :> {1}{2}{3}".format(bcolors.normal, bcolors.yellow, text, bcolors.end, brain.session_name)
        voice.text_to_speech(text)


def speech_to_text():
    ears.record_to_file(ears.wavfile)

    recognizing = ears.decode_speech(
        ears.acoustic_model_directory,
        ears.language_model_file,
        ears.dictionary_file,
        ears.wavfile
    )
    if not recognizing == '':
        print bcolors.normal + "\bHuman :> " + bcolors.yellow + recognizing + bcolors.end
    os.remove(ears.wavfile)
    return recognizing


def main():
    brain.load_brain()
    brain.load_session()
    reload_modules_text = [
        "né le jour les modules",
        "les jours les modules",
        "les jour les modules",
        "mis à jour des modules",
        "mis à jour les modules",
        "mise jour des modules",
        "mise à jour des modules",
        "mise à jour les modules",
        "mais un jour les modules",
        "mais un jour des modules",
        "mais le jour les modules",
        "mais à ce jour les modules",
        "mais le jour des modules",
        "mais le jour les modules",
        "mais pour les modules",
        "recharger modules",
        "recharger les modules",
        "en charge des modules",
        "charges les modules",
        "recherché modules",
        "mais sur les modules",
        "rogers les modules",
        "on recharge les modules",
        "recherche module",
        "neuf jours les modules",
        "les agents des modules",
        "recherche les modules",
        "bien_sûr les modules",
        "mais sur les modes",
        "mais un jour les modes",
        "mais un jour lin",
        "mais sur le module",
        "né à jour les modules",
        "mais un jour le module",
        "mais sur le modèle",
        "les agents de modules",
        "mais un jour modules",
        "modules reload"
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

    # Queue
    queue_eyes = Queue()
    queue_ears = Queue()
    queue_mounth = Queue()

    # Worker's
    little_alice_eyes = Process(target=eyes.run, args=(queue_eyes,))
    little_alice_ears_decode_speech = Process(target=ears, args=(queue_ears,))
    little_alice_mounth = Process(target=text_to_speech, args=(queue_mounth,))

    little_alice_eyes.start()
    try:
        while True:
            set_prompt_type(1)
            recognised = speech_to_text()

            if not recognised == '':
                # os.system(cmd % brain.kernel.respond(recognised, brain.session_name))
                text_to_speech(brain.kernel.respond(recognised, brain.session_name))

            if recognised in reload_modules_text:
                brain.reload_modules()
                text_to_speech('C\'est fait')
            # elif recognised == 'rouge':
            #     queue_eyes.put('red')
            # elif recognised == 'blue':
            #     queue_eyes.put('blue')
            # elif recognised == 'cyan':
            #     queue_eyes.put('cyan')
            elif recognised == 'je vais me coucher':
                text_to_speech('OK, veux tu que je ferme tout ?')
                set_prompt_type(1)
                recognised = speech_to_text()
                if recognised == 'oui':
                    text_to_speech('OK, je fais ça')
                    brain.save_session()
                    os.system('sudo /sbin/shutdown -h 0')
                    os.system(sys.exit(0))
            elif recognised in exit_text:
                text_to_speech('Au revoir')
                brain.save_session()
                os.system(sys.exit(0))

    except KeyboardInterrupt:
        pass
    finally:
        little_alice_eyes.terminate()
        little_alice_eyes.join()
        os.system(sys.exit(0))


if __name__ == '__main__':
    main()
