Role Name
=========

sqmail-server role have goal to install and configure a s/qmail server from "fehcom" design.

    s/qmail (pronounced skew-mail) is a Mail Transfer Agent (MTA) based on Qmail
    suited for high-speed and confidential email transport over IPv4 and IPv6 networks.

For more informations: http://fehcom.de/sqmail/sqmail.html

That role by default follow exactelly the design describ by fehcom, but convert a maximum of path, values, file for have a dynamic setting. By exemple all UID, GID, path, can be change , or be different by machine (not sure it's usefull).

It role is part of Galaxie design, if you like it please not forke, try to propose a patch or e-mail me.
I'm not part of "fehcom" team, i'm just a humain it focus on Galaxie design devellopement, you are free to use my work without any warranty , may be in 50 years that work will be out-dated who know ...

By default that role will done the same result as the "fehcom" documentation, that mean after all conditional test and teamplate application under Ansible all scripts, configuration files will use default as descript on "fehcom" documentation.
All the power/interest of that role is the capability to use "host_vars" or "group_vars" and custom every path or values, the configuration will stay automaticlly consistent.
Unfortunally that a feature it come with Ansible, then don't be usefull for "s/qmail" project, except the role it self ...

I do my best for workarround troubles without need to touch "s/qmail" source, actually "s/qmail have troubles it not permit easy automation.

my list of thins to repport to "fehcom" team:
- package/man error with qmail-local
- installation script ignore conf-svcdir value
- script .run don't take advantage of ucspi-tcp6 conf-tcpbin file
- 64 / 32 bit auto detection is aviable for s/qmail but put in hard value for ucspi-tcp6, may be auto for ucspi-ssl, and don't care about cdb
- (list not close)

That role try to fixe (by the hard way) or reduse the impact of they troubles

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

run_log script:
- Use Ansible templating system for write the script from "./defaults/main.yml" variable file
- Value "/var/log" have been replace by "{{ glx_multilog_dir }}"
- Value "/var/log" inside "conf-log" file have been replace by {{ glx_multilog_dir }}
- Value "nofiles" it make reference to nofiles group have been replace by {{ glx_sqmail_groups.nofiles.gname }}, "conf-ids" and "conf-group" use the same methode then the log script recive consitent information.
- Value "qmaill" it make reference to sqmail Log user have been replace by {{ glx_sqmail_ids.qmaill.uname }}, "conf-ids" and "conf-group" use the same methode then the log script recive consitent information.
todo:
- Reference to "multilog" group , it make reference to daemontools group name should be dynamic; actually Galaxie design use daemontools Debian package but soon, daemontools will be dedicated to s/qmail, then the multilog username or UID will be under s/qmail control.

run_pop3d script:
- Value "/var/qmail" have been replace by {{ glx_qmail_dir }}
- Value "Maildir" it suppose to be the maildirname have been replace by {{ glx_sqmail_maildirname }} it store "Mailbox", {{ glx_sqmail_maildirname }} is use during "defaultdelivery" control file creation, like that glx_sqmail_control_defaultdelivery: "./{{ glx_sqmail_maildirname }}/"
todo:
- HOSTNAME should store same value a control/me file

run_pop3sd script:
- Value "/var/qmail" have been replace by {{ glx_qmail_dir }}
- Value "Maildir" it suppose to be the maildirname have been replace by {{ glx_sqmail_maildirname }} it store "Mailbox", {{ glx_sqmail_maildirname }} is use during "defaultdelivery" control file creation, like that glx_sqmail_control_defaultdelivery: "./{{ glx_sqmail_maildirname }}/"
todo:
- HOSTNAME should store same value a control/me file

ESMTP.run script:
- Hard value "/var/qmail" have been replace by {{ glx_qmail_dir }} then permit to follow the global setting
- Hard value "qmaild" have been replace by {{ glx_sqmail_ids.qmaild.uname }} then permit to follow the global setting
Role Variables
--------------

A maxium of variables have been set that for permit fine tuning inside host_var or group_var

Here the lists:
yet (You can found it on ./defaults/main.yml)

we have make our maximum for have explicite variable name, that should minimize the need of details.


Dependencies
------------
"daemontools" from D. J. Bernstein (https://cr.yp.to/daemontools.html) should be install frist.

By default the role use Debian packages "daemontools" and "daemontools-run" then have default Debian system directory path, it's the root cause about why everything is dynamic on that role.

by exemple: glx_supervise_dir: "/var/lib/supervise" it the true Debian path, /service is /etc/service

Example Playbook
----------------
as do by ../sqmail-server.yml all default value are inside ./defaults/main.yml file

    - hosts: sqmail-servers
    
      roles:
         - sqmail-server

License
-------

GPL 3

Author Information
------------------

Tuux from rtnp.org