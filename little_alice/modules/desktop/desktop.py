#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'

import getopt
import os
import sys
import subprocess
import locale
import random

locale.setlocale(locale.LC_ALL, '')

version = '1.0'
verbose = False
output_filename = 'default.out'
browser = False
email = False
terminal = False

it_done = [
    "C'est fait",
    "OK",
    "Et voilà",
    "Voilà",
    "On fait ça"
]

options, remainder = getopt.gnu_getopt(
    sys.argv[1:], 'o:v', ['output=',
                          'verbose',
                          'version=',
                          'browser',
                          'email',
                          'terminal'
                          ]
)


def check_terminal():
    if not which('gnome-terminal'):
        print "Gnome Terminal n'est pas installé"
        sys.exit(1)
    else:
        return which("gnome-terminal")


def check_browser():
    if not which("firefox"):
        print "Firefox n'est pas installé"
        sys.exit(1)
    else:
        return which("firefox")


def check_email():
    if not which("thunderbird"):
        print "Thunderbird n'est pas installé"
        sys.exit(1)
    else:
        return which("thunderbird")


def which(program):
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


def start_terminal(terminal_path):
    command = list()
    command.append(terminal_path)
    try:
        output = subprocess.check_output(command)
        it_have_error = 0
    except:
        it_have_error = 1
    if it_have_error:
        print("Impossible")
    else:
        print(random.choice(it_done))

def start_browser(browser_path):
    command = list()
    command.append(browser_path)
    try:
        output = subprocess.check_output(command)
        it_have_error = 0
    except:
        it_have_error = 1
    if it_have_error:
        print("Impossible")
    else:
        print(random.choice(it_done))

def start_email(email_path):
    command = list()
    command.append(email_path)
    try:
        output = subprocess.check_output(command)
        it_have_error = 0
    except:
        it_have_error = 1
    if it_have_error:
        print("Impossible")
    else:
        print(random.choice(it_done))

def start_under_terminal(terminal_path, command):
    cmd = list()
    cmd.append(terminal_path)
    cmd.append("-e")
    cmd.append("\"" + command + "\"")
    try:
        output = subprocess.check_output(cmd)
        it_have_error = 0
    except:
        it_have_error = 1

    if it_have_error:
        print("Impossible")
    else:
        print(random.choice(it_done))



for opt, arg in options:
    if opt in ('-o', '--output'):
        output_filename = arg
    elif opt in ('-v', '--verbose'):
        verbose = True
    elif opt == '--version':
        version = arg
    elif opt == '--browser':
        browser_path = check_browser()
        browser = True
    elif opt == '--email':
        email_path = check_email()
        email = True
    elif opt == '--terminal':
        terminal = True

terminal_path = check_terminal()

if terminal:
    start_terminal(terminal_path)
if browser:
    start_browser(browser_path)
if email:
    start_under_terminal(terminal_path, email_path)