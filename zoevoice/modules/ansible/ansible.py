#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tuxa'

import getopt
import os
import sys
import subprocess
import locale
import random

locale.setlocale(locale.LC_ALL, '')

#######################################
######DEFINE SOME BASIC VARIABLES######
#######################################
version = '1.0'
verbose = False
upgrade_a_host = False
upgrade_all_hosts = False
restart_pbx_servers = False
restart_pvr_servers = False
restart_medias_servers = False


# User Setting #
################

playbook_dir = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../playbooks")
)
inventory_file = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../host.inventory")
)

playbook_galaxie_upgrade_filename = 'galaxie-upgrade.yml'
playbook_restart_pbx_servers_filename = 'galaxie-restart-pbx-servers.yml'
playbook_restart_pvr_servers_filename = 'galaxie-restart-pvr-servers.yml'
playbook_restart_medias_servers_filename = 'galaxie-restart-medias-servers.yml'

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
                          'upgrade-host=',
                          'upgrade-all-hosts',
                          'restart-pbx-servers',
                          'restart-pvr-servers',
                          'restart-medias-servers'
                          ]
)


# Function it return ansible-playbook path or exit
def check_ansible_playbook():
    if not which('ansible-playbook'):
        print "Ansible: ansible-playbook n'est pas installé"
        sys.exit(1)
    else:
        return which("ansible-playbook")


# Function it return Gnome-terminal path or exit
def check_terminal():
    if not which('gnome-terminal'):
        print "Gnome Terminal n'est pas installé"
        sys.exit(1)
    else:
        return which("gnome-terminal")


# Function it search for the path of a program
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


# Function it start under a terminal ansible_command_line
def start_ansible_under_terminal(terminal_path, command):
    cmd = list()
    cmd.append(terminal_path)
    cmd.append("-e")
    cmd.append(command)
    try:
        output = subprocess.check_output(cmd)
        it_have_error = 0
    except:
        it_have_error = 1

    if it_have_error:
        print("Impossible")
    else:
        print(random.choice(it_done))


def creat_ansible_command_line(ansible_playbook_path, inventory_file, playbook_dir, playbook_filename):
    ansible_command_line = ""
    ansible_command_line += ansible_playbook_path
    ansible_command_line += " "
    ansible_command_line += "-i"
    ansible_command_line += " "
    ansible_command_line += inventory_file
    ansible_command_line += " "
    ansible_command_line += os.path.join(playbook_dir, playbook_filename)
    return ansible_command_line

terminal_path = check_terminal()
ansible_playbook_path = check_ansible_playbook()

for opt, arg in options:
    if opt in ('-o', '--output'):
        output_filename = arg
    elif opt in ('-v', '--verbose'):
        verbose = True
    elif opt == '--version':
        version = arg
    elif opt == '--upgrade-host':
        host_to_upgrade = arg
        upgrade_a_host = True
        ansible_command_line = creat_ansible_command_line(
            ansible_playbook_path,
            inventory_file,
            playbook_dir,
            playbook_galaxie_upgrade_filename
        )
        ansible_command_line += " "
        ansible_command_line += " --limit="
        ansible_command_line += host_to_upgrade
    elif opt == '--upgrade-all-hosts':
        upgrade_all_hosts = True
        ansible_command_line = creat_ansible_command_line(
            ansible_playbook_path,
            inventory_file,
            playbook_dir,
            playbook_galaxie_upgrade_filename
        )
    elif opt == '--restart-pbx-servers':
        restart_pbx_servers = True
        ansible_command_line = creat_ansible_command_line(
            ansible_playbook_path,
            inventory_file,
            playbook_dir,
            playbook_restart_pbx_servers_filename
        )
    elif opt == '--restart-pvr-servers':
        restart_pvr_servers = True
        ansible_command_line = creat_ansible_command_line(
            ansible_playbook_path,
            inventory_file,
            playbook_dir,
            playbook_restart_pvr_servers_filename
        )
    elif opt == '--restart-medias-servers':
        restart_medias_servers = True
        ansible_command_line = creat_ansible_command_line(
            ansible_playbook_path,
            inventory_file,
            playbook_dir,
            playbook_restart_medias_servers_filename
        )


if restart_pbx_servers:
    start_ansible_under_terminal(terminal_path, ansible_command_line)
elif restart_pbx_servers:
    start_ansible_under_terminal(terminal_path, ansible_command_line)
elif restart_medias_servers:
    start_ansible_under_terminal(terminal_path, ansible_command_line)
elif upgrade_all_hosts:
    start_ansible_under_terminal(terminal_path, ansible_command_line)