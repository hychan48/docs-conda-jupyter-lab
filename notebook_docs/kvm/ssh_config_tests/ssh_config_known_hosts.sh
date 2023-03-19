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


# Generate known_hosts
ssh-keyscan -t rsa kvm.mshome.net
ssh-keyscan -t rsa target_name
kvm.mshome.net,192.168.49.41 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBPH5lpPXA50HP1H5OnUb4HcXWA28qZyozEGW0SNNQhVhlqgmz/bdLicfAd5K0AYviiN5IEtgesySXgqwq0iIs+c=
# copy and paste the sha2 part of the output... can maybe auto do this
# discovvery complete. paramiko is shit. doesnt look at config file properly