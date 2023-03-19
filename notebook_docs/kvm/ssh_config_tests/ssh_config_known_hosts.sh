#!/bin/bash
# need to change config
# https://linux.die.net/man/1/ssh
# https://linux.die.net/man/5/ssh_config
# ssh -F configfile 
clear
echo `date`
rm -f ~/.ssh/known_hosts.*
ls ~/.ssh/
# ssh -F know_hosts.ssh.config root@192.168.122.1
# found key in known_hosts....
# ps1 - windows has to use ed key
# ssh-keygen -t ed25519
ssh -F /root/make_hal9000/ssh_config_tests/know_hosts.ssh.config root@localhost 'hostname'
ssh -F /root/make_hal9000/ssh_config_tests/know_hosts.ssh.config root@192.168.122.1 'hostname'
ssh -F /root/make_hal9000/ssh_config_tests/know_hosts.ssh.config jason@192.168.122.77 'hostname'

# ssh -F /root/make_hal9000/ssh_config_tests/know_hosts.ssh.config root@127.0.0.1 'hostname' # this doesnt work
# host key verification failed?
#  ssh -vv localhost
# windows
