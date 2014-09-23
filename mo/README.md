Stage 0
=======
Where the magic begins
----------------------


0 - ZOE is Open and Extendable
------------------------------

When adding a freshly installed machine to the design:

* name it in your head, let's name it _alice_ for this example.
* create a ssh key for ansible access:
```
ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa.alice
```

* place its reference in the desired group in host.inventory
  * it's even better if you already have a dnsmasq in your network so you can refer to this 
  machine by its network official name, configured by a MAC address matching in the DHCP.

* install an access for zoe by running:

```
ansible-playbook -i host.inventory galaxie-0-00-zoe.yml --limit=$MY_NEW_MACHINE_REF --user=$DEFAULT_USER_WITH_SUDO --ask-pass
```

that will create standardized group and user for the others playbook to run smoothly. 