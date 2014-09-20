#! /bin/bash
ssh zoe "sudo apt-get install -y python"
ansible-playbook galaxie_ssh.yml
ansible-playbook galaxie_motd.yml
ansible-playbook galaxie_ntp.yml
ansible-playbook install-packages-cli.yml
ansible-playbook galaxie_bashrc.yml
ansible-playbook galaxie_setting_vim.yml
ansible-playbook galaxie_dvbhdhomerun.yml
ansible-playbook galaxie_tvheadend.yml
ansible-playbook galaxie_zfsonlinux.yml
