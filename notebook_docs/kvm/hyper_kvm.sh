# old
# Host 192.168.122.*
# #    HostName kvm.mshome.net
# #    User jason
#    IdentityFile ~/.ssh/id_rsa
#    StrictHostKeyChecking No
#    UserKnownHostsFile=/dev/null

# USE THIS ONE
initialize(){
    # sudo apt -f install libvirt-daemon-system virtinst
    # sudo apt -f install cloud-init # doesnt give me cloud-localsd, but gives me validator
    # https://command-not-found.com/cloud-localds


    # 1. Download iso / probably need to copy it or something
    wget https://cloud-images.ubuntu.com/releases/focal/release/ubuntu-20.04-server-cloudimg-amd64.img
    # not the kvm image i think (usb image)
    # 2. iso to qcow2
    # qemu-img create -b ubuntu-20.04-server-cloudimg-amd64.img -f qcow2 -F qcow2 hal9000.qcow2 10G
    qemu-img create -b /var/lib/libvirt/images/ubuntu-20.04-server-cloudimg-amd64.img -f qcow2 -F qcow2 hal9000.qcow2 10G
    apt-get install -f cloud-image-utils
    # 3. seed img / assuming user-data.yaml is created
    # genisoimage -output cidata.iso -V cidata -r -J user-data.yaml metadata.yaml
    # don't use genisoimage... or maybe wrong flags use cloud-localds to create seed

    cp ubuntu-20.04-server-cloudimg-amd64.img /var/lib/libvirt/images/
    cp /root/ubuntu-22.04-minimal-cloudimg-amd64.img /var/lib/libvirt/images/
    qemu-img create -b /var/lib/libvirt/images/ubuntu-22.04-minimal-cloudimg-amd64.img -f qcow2 -F qcow2 hal9000.qcow2 10G

}
notes(){
    default_lib_virt=/var/lib/libvirt
    default_lib_virt=/var/lib/libvirt/images
    # default_lib_virt=/var/lib/libvirt/qemu
    cd /var/lib/libvirt/images
    chown libvirt-qemu:kvm *

}
#--------------
# https://stackoverflow.com/questions/29137679/login-credentials-of-ubuntu-cloud-server-image
# i think it was this one that worked then
# cloud-localds seed.img user-data.yaml metadata.yaml

if cloud-init schema --config-file user-data.yaml ; then
    echo "Command succeeded"
else
    echo "Command failed"
    exit(1)
fi

cloud-localds seed.img user-data.yaml metadata.yaml

mkdir -p /var/lib/libvirt/images/vm/hal9000

cp hal9000.qcow2 /var/lib/libvirt/images/vm/hal9000 # really a qcow2.... should rename
cp seed.img /var/lib/libvirt/images/vm/hal9000
# cp /var/lib/libvirt/images/ubuntu-20.04-server-cloudimg-amd64.img /vm/hal9000
chown libvirt-qemu:kvm /var/lib/libvirt/images/vm/hal9000/*

# from my old script
# --network type=network,source=default,model=virtio \
# --network bridge=virbr0,model=virtio \ # their example
virt-install --name=hal9000 --ram=2048 --vcpus=2 --import \
    --disk path=/var/lib/libvirt/images/vm/hal9000/hal9000.qcow2,format=qcow2 \
    --disk path=/var/lib/libvirt/images/vm/hal9000/seed.img,device=cdrom \
    --os-variant=ubuntu20.04 \
    --network type=network,source=default,model=virtio \
    --graphics vnc,listen=0.0.0.0 --noautoconsole
    # --os-variant=ubuntu22.04 \
# virsh --connect qemu:///system start hal9000
# 52:54:00:43:a3:34

# ssh root@`virsh domifaddr ub1 | awk '/ipv4/ {print $4}' | awk -F'/' '{print $1}'`
# ssh jason@`virsh domifaddr hal9000 | awk '/ipv4/ {print $4}' | awk -F'/' '{print $1}'`
# ssh -i ~/.ssh/id_rsa jason@`virsh domifaddr hal9000 | awk '/ipv4/ {print $4}' | awk -F'/' '{print $1}'`

# https://serverfault.com/questions/426394/how-to-check-if-an-rsa-public-private-key-pair-match
# #cloud-config
# username: ubuntu
# password: ubuntu
# chpasswd: { expire: False }
# ssh_pwauth: True
# check hostnames
# virsh net-dhcp-leases default
# virsh net-dumpxml default


