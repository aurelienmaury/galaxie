Role Name
=========

Qmail-server role have goal to install and configure a s/qmail server from fehcom design.

s/qmail (pronounced skew-mail) is a Mail Transfer Agent (MTA) based on Qmail suited for high-speed and confidential email transport over IPv4 and IPv6 networks.
More informations:
http://fehcom.de/sqmail/sqmail.html

Requirements
------------
it should work on Debian's familly GNU/Linux distribution.
The role install it self requirements

The role use the daemons-tool provide by Debian packages

Features
--------
each compoments:
- tasks/*.yml file have minimal value set in hard everything is editable via defaults/main.yml file.

ucspi-tcp6:
- auto 32/64 bit configuration by x64 detection and switch play with -m64 on conf-ld files

s/qmail:
- conf-log, get value from "glx_multilog_dir" var
- scripts get all value from settings
- conf-ids, conf-group -  by edit a value inside defaults/main.yml it will automatiquelly make consistant setting.

Role Variables
--------------

A maxium of variables have been set that for permit fine tuning inside host_var or group_var

Here the lists:
yet (You can found it on ./defaults/main.yml)

we have make our maximum for have explicite variable name, that should minimize the need of details.


Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: sqmail-servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

GPL 3

Author Information
------------------

Tuux from rtnp.org