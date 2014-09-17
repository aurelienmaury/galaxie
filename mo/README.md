Stage 0
=======
Where the magic begins
----------------------


0 - ZOE is Open and Extendable
------------------------------

When adding a freshly installed machine to the design:

* place its reference in the desired group in host.inventory
* install an access for zoe by running:

```
ansible-playbook -i host.inventory galaxie-0-00-zoe.yml --limit=$MY_NEW_MACHINE_REF --user=$DEFAULT_USER_WITH_SUDO --ask-pass
```

that will create standardized group and user for the others playbook to run smoothly. 