#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'tuxa@rtnp.org'

import sys
import os.path
from body.brain import Brain
from body.voice import Voice
from body.ears import Ears

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
        print "{0}\b{4} :> {1}{2}{3}".format(bcolors.normal, bcolors.yellow, text, bcolors.endc, brain.session_name)
        voice.text_to_speech(text)


def stt():
    ears.record_to_file(ears.wavfile)
    recognizing = ears.decode_speech(
        ears.acoustic_model_directory,
        ears.language_model_file,
        ears.dictionary_file,
        ears.wavfile
    )
    if not recognizing == '':
        # recognizing.decode('iso-8859-1').encode('utf8')
        # recognizing.decode('utf8').encode('iso-8859-1')
        print bcolors.normal + "\bHuman :> " + bcolors.yellow + recognizing + bcolors.endc
    os.remove(ears.wavfile)
    return recognizing


def main():
    brain.load_brain()
    brain.load_session()
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

        tts(brain.kernel.respond(recognised, brain.session_name))

        if recognised in reload_modules_text:
            brain.reload_modules()
            tts("C'est fait")
        elif recognised == "je vais me coucher":
            tts("OK, veux tu que je ferme tout ?")
            set_prompt_type(1)
            recognised = stt()
            if recognised == "oui":
                tts("OK, je fais ça")
                brain.save_session()
                os.system("sudo /sbin/shutdown -h 0");
                os.system(sys.exit(0));
        elif recognised in exit_text:
            tts("Au revoir")
            brain.save_session()
            os.system(sys.exit(0));
            # elif recognised in upgrade_text:
            #     os.system(galaxie_update_hosts_cmd)
            #     tts("Je lance ça")


if __name__ == '__main__':
    main()
