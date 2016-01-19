ZOE is Open and Extendable
==========================

## DISCLAIMER

When you add a new host, you need to play a bit with ansible-playbook options to initiate the first connection
by password. You could have either:

* root account with password
* user account with sudo already installed
* user account with su password to supply

Use the right combination of options to get the initial connection. This first steps are to normalize ZOE access
for the other playbooks. The ```sudo: yes``` at the top of the playbook, and options like 
```[ --su, --ask-su-pass, --ask-pass]``` should help you achieve initial connection.

## Initial setup

When adding a freshly installed host to the design:

* name it in your head, let's name it _elvira_ for this example.

* place its reference in the desired group in host.inventory with a host var called _newKey_ pointing to a local private key file. 
Doesn't matter if this file does not exist yet, it will be generated soon.

```
# it's even better if you already have a dnsmasq in your network so you can refer to this 
# host by its network official name, configured by a MAC address matching in the DHCP.

[galaxie]
192.168.0.42 newKey=~/.ssh/id_rsa.elvira
```

* we assume that you already have a root account (or a sudo-all account on elvira).
* install an access for ZOE by running:

Notes: Unfortunally actually the installation methode is not finish, we plan for a dedicted application, but yet , you have to do it manually.
Fllow they step:
1) Install a Debian system
2) Install with root user "sudo" command line with "apt-get install sudo" inside a terminal
```
apt-get install sudo
```
3) With you favorite editor add that line on /etc/sudoers 
```
YOU_SUPER_USER_YOU_WANT_USE_FOR_INSTALL_ZOE ALL=(ALL) NOPASSWD: ALL
```
4) Now start our integration playbook.
```
ansible-playbook -i ../host.inventory galaxie-zoe-integration.yml --user=$DEFAULT_USER_WITH_SUDO  --ask-pass  --limit 192.168.0.42
ansible-playbook -i ../host.inventory galaxie-zoe-integration.yml --user=$DEFAULT_USER_WITH_SUDO  --ask-pass -c paramiko --limit 192.168.0.42
```

* you will be prompted for your password and the playbook will setup everything for ZOE access.
* when finished, return to the inventory and change the name of the variable like this:

```
[galaxie]
192.168.0.42 ansible_ssh_private_key_file=~/.ssh/id_rsa.elvira
```

* Your elvira is now ready to be managed by ZOE.

## Key rotation

* Go to your inventory and add a newKey variable for the host you want to rotate key:

```
[galaxie]
192.168.0.42 ansible_ssh_private_key_file=~/.ssh/id_rsa.elvira newKey=~/.ssh/id_rsa.elvira-newer
```

* Apply the playbook:

```
ansible-playbook -i host.inventory galaxie-zoe_access.yml --user=zoe --limit=192.168.0.42
```

* Make the newKey value become the ansible_ssh_private_key_file value:

```
[galaxie]
192.168.0.42 ansible_ssh_private_key_file=~/.ssh/id_rsa.elvira-newer
```
* Done.

# User interface simplification proposal

* galaxie swallow $TARGET_GROUP $HOST_NAME_OR_IP : prompts for sudoable user, adds host in the right group in host inventory, fills newKey value, launches galaxie-zoe_access.yml, renames newKey to ansible private key.

integration - ntp - sshd

# TODO mention dans le motd : accès non autorisé, pas autorisé
