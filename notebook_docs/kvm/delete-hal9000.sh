#/bin/bash
${$1:-hello}
VM_NAME=hal9000
echo $VM_NAME
virsh shutdown --domain $VM_NAME
read -t 10
virsh undefine --domain $VM_NAME
# rm -f /vm/hal9000/*
# mkdir -p /var/lib/libvirt/images/vm/hal9000
rm -f /var/lib/libvirt/images/vm/hal9000/*

##/bin/bash
## maybe source a file for all? - or just do it in python for now
#VM_NAME=${1:-hal9000}
#echo $TMP