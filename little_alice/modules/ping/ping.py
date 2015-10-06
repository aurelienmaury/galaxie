#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it published under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved
__author__ = 'Tuux'

# No supported by Windows
import getopt
import random
import sys
import commands

check_internet_hostname = "www.wikipedia.org"

version = '1.0'
verbose = False
check_internet_connection = False

internet_is_down = [
    "La connection internet est morte ",
    "Nous sommes coupé du monde extérieur ",
    "Il n y a pas de connectivitée à Internet",
    "Il me semble que la connection est morte",
    "La ligne est tombée"
]

internet_is_up = [
    'Oui, La connection à Internet est opérationelle. ',
    "Oui, Tout à l'air de fonctionner normalment. ",
    "Oui, Les paramètres sont normaux. ",
    "Oui, Je suis à même de joindre le monde extérieur. ",
    "Oui, J'ai la connectivitée au monde extérieur",
    "Oui, Wikipédia a répondu à mes solicitations. "
]


options, remainder = getopt.gnu_getopt(
    sys.argv[1:],
    'o:v',
    {'output=',
     'verbose',
     'version=',
     'check-internet-connection'}
)

for opt, arg in options:
    if opt in ('-o', '--output'):
        output_filename = arg
    elif opt in ('-v', '--verbose'):
        verbose = True
    elif opt == '--version':
        version = arg
    elif opt == '--check-internet-connection':
        check_internet_connection = True


def print_check_internet_connection():
    cmd = 'ping -c 1'
    cmd += ' '
    cmd += check_internet_hostname
    status, output = commands.getstatusoutput(cmd)
    # and then check the response...
    if status == 0:
        print(random.choice(internet_is_up))
    else:
        print(random.choice(internet_is_down))

if check_internet_connection:
    print_check_internet_connection()
