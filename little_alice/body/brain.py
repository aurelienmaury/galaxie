#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'

import os
import aiml
import marshal


class Brain(object):
    def __init__(self, modules_dir, brains_dir):
        self.modules_dir = modules_dir
        self.brains_dir = brains_dir
        self.lang = 'fr_FR'
        self.kernel = aiml.Kernel()
        self.brain_file = "brain.br"
        self.session_file = "session.ses"
        self.session_name = "Alice"

    def load_module(self, module_name):
        path = os.path.join(
            os.path.join(self.modules_dir, module_name),
            self.lang
        )
        os.chdir(path)
        list_files = os.listdir(".")
        for item in list_files:
            if item.endswith('.aiml'):
                self.kernel.learn(os.path.join(path, item))

    def reload_modules(self):
        os.chdir(self.brains_dir)
        os.remove(self.brain_file)
        self.load_brain()
        self.save_session()

    def load_brain(self):
        """ read dictionary and create brain in file little_alice.brp"""
        os.chdir(self.brains_dir)
        if os.path.isfile(self.brain_file):
            self.kernel.bootstrap(brainFile=self.brain_file)
        else:
            self.load_module('little_alice')
            self.load_module('date')
            self.load_module('meteo')
            self.load_module('desktop')
            self.load_module('ansible')
            #self.load_module('alice')
            os.chdir(self.brains_dir)
            self.kernel.setPredicate("master", self.session_name)
            self.kernel.saveBrain(self.brain_file)  # save new brain
        # name of bot
        self.kernel.setBotPredicate('name', self.session_name)

    def load_session(self):
        os.chdir(self.brains_dir)
        if os.path.isfile(self.session_file):
            session_file = file(self.session_file, "rb")
            session = marshal.load(session_file)
            for pred, value in session.items():
                self.kernel.setPredicate(pred, value, self.session_name)

    def save_session(self):
        os.chdir(self.brains_dir)
        session = self.kernel.getSessionData(self.session_name)
        session_file = file(self.session_file, "wb")
        marshal.dump(session, session_file)
        session_file.close()