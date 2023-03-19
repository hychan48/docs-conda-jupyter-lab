#!/bin/bash
clear
echo `date`
# Virt Install
UB='ub'
ub_range=(1 2)
SSD=10G
RAM=2048
VCPUS=1
OS_VARIANT='ubuntu20.04' # maybe combine this into a lookup table later
URL_TO_DOWNLOAD_IMG="https://cloud-images.ubuntu.com/releases/focal/release/ubuntu-20.04-server-cloudimg-amd64.img"
FILE_NAME=$(basename $URL_TO_DOWNLOAD_IMG) # override if not the same as url
# ubuntu-20.04-server-cloudimg-amd64.img

#  /var/lib/libvirt/images #root
#  ├── /bases
#  │   ├── # qcow will reference this
#  │   └── ubuntu-20.04-server-cloudimg-amd64.img
#  └── /qcows
#      └── /vms-ub
#          ├── ub1.qcow2
#          ├── ub2...
#          └── ub<n>
# METADATA # this script is generating it... maybe later we can merge them
## meta-data.yaml # dont touch my metadata.yaml is for reference
# user-data.yaml is assumed to be here
IMG_PATH="/var/lib/libvirt/images"
# only downloads if file doesnt exist

# STATES / VAR RUNTIME
ub_names=() # will be populated (ub1 ub2)
img_file_path="$IMG_PATH/bases/$FILE_NAME"
qcows_vms_prefix="$IMG_PATH/qcows/vms-$UB"

# Utils ---------------
check_user_data_schema () {
  if cloud-init schema --config-file user-data.yaml ; then
    echo "1. Check user-data.yaml"
  else
    echo "Command failed Check user-data.yaml">2%
    exit 1
  fi

}
# sample for copy / pasta
if_file_exist () {
  if [ -z "$1" ]
  then
    echo "\$1 is empty... exiting" >&2
    exit 1
  fi
  echo "$@"

}
check_range(){
#  echo "${#ub_range[@]}" # this is the length
  if [ 2 != "${#ub_range[@]}" ]
  then
    exit 1
    echo "ub_range is not two. i.e. (1 2) exiting..." >&2
  fi

  for i in `seq ${ub_range[0]} ${ub_range[1]}`
  do
      # Create the filename
      ub_names+=("$UB$i")
  done
#  echo "${ub_names[*]}"
  # sets ub_names to (ub1 ub2)
}


generate_meta_data_yaml () {
#  instance-id: hal9000
#  local-hostname: hal9000
  vm_name_hostname=$1
  echo "instance-id: $vm_name_hostname" > meta-data.yaml
  echo "local-hostname: $vm_name_hostname" >> meta-data.yaml

}

ssh_into_vm (){
  vmn=$1
#  ssh -i ~/.ssh/id_rsa jason@`virsh domifaddr ub1 | awk '/ipv4/ {print $4}' | awk -F'/' '{print $1}'`
  ssh -i ~/.ssh/id_rsa jason@`virsh domifaddr "$vmn" | awk '/ipv4/ {print $4}' | awk -F'/' '{print $1}'`
}
print_network () {
  virsh net-dhcp-leases default
}
dev_shutdown_all () {

  for VM_NAME in "${ub_names[@]}"
  do
     :
    virsh shutdown --domain $VM_NAME

  done
}
dev_delete_images () {

  # might need a for loop
  for VM_NAME in "${ub_names[@]}"
  do
     :
    virsh shutdown --domain $VM_NAME
    read -t 10
    virsh undefine --domain $VM_NAME
     # maybe check if exists....
     # do whatever on "$val" here
  done

  # at the end...
  rm -rf "/var/lib/libvirt/images/qcows/vms-$UB"
  # clear macs... probably better way. peter had some script
  rm /var/lib/libvirt/dnsmasq/virbr0.*
  virsh net-destroy default && virsh net-start default
  service libvirtd restart
}
#----------------------
# 1. Install Packages on kvm if not installed
install_packages(){
     sudo apt -f install libvirt-daemon-system virtinst
     sudo apt -f install cloud-init # doesnt give me cloud-localsd
     sudo apt-get install -f cloud-image-utils
}
initialize_folder_structure(){
  mkdir -p $IMG_PATH/bases
  mkdir -p $IMG_PATH/qcows/vms-$UB
  chown -R libvirt-qemu:kvm $IMG_PATH/bases
  chown -R libvirt-qemu:kvm $IMG_PATH/qcows/vms-$UB
}

# shellcheck disable=SC2120
check_base_img_or_download(){
#  tmp=$(ls "$IMG_PATH/bases/$FILE_NAME")
#  FILE="$IMG_PATH/bases/$FILE_NAME"
  FILE="$img_file_path"
  if test -f "$FILE"; then
    echo "2. Img exists... $FILE"
  else
      wget $URL_TO_DOWNLOAD_IMG
      mv "$FILE_NAME" "$IMG_PATH/bases/"
      chown libvirt-qemu:kvm "$IMG_PATH/bases/*"
  fi



#  wget $URL_TO_DOWNLOAD_IMG
#  mv basename $URL_TO_DOWNLOAD_IMG
#  chown -R libvirt-qemu:kvm $IMG_PATH/bases/*

}

_initialize_download_images(){

    # https://command-not-found.com/cloud-localds
    # 1. Download iso / probably need to copy it or something
    wget https://cloud-images.ubuntu.com/releases/focal/release/ubuntu-20.04-server-cloudimg-amd64.img
    # not the kvm image i think (usb image)
    # 2. iso to qcow2
    # qemu-img create -b ubuntu-20.04-server-cloudimg-amd64.img -f qcow2 -F qcow2 hal9000.qcow2 10G
    qemu-img create -b /var/lib/libvirt/images/ubuntu-20.04-server-cloudimg-amd64.img -f qcow2 -F qcow2 hal9000.qcow2 10G

    # 3. seed img / assuming user-data.yaml is created
    # genisoimage -output cidata.iso -V cidata -r -J user-data.yaml metadata.yaml
    # don't use genisoimage... or maybe wrong flags use cloud-localds to create seed

    cp ubuntu-20.04-server-cloudimg-amd64.img /var/lib/libvirt/images/
    cp /root/ubuntu-22.04-minimal-cloudimg-amd64.img /var/lib/libvirt/images/
    qemu-img create -b /var/lib/libvirt/images/ubuntu-22.04-minimal-cloudimg-amd64.img -f qcow2 -F qcow2 hal9000.qcow2 10G

}

createqcow (){
#  qemu-img create -b /var/lib/libvirt/images/ubuntu-20.04-server-cloudimg-amd64.img -f qcow2 -F qcow2 hal9000.qcow2 10G
  vmn=$1
  generate_meta_data_yaml $vmn
  seed="$vmn.seed.img" # used in install_vm too... maybe cleanup
  qcow="$vmn.qcow2"
  cloud-localds "$seed" user-data.yaml meta-data.yaml
  qemu-img create -b "$img_file_path" -f qcow2 -F qcow2 "$qcow" $SSD
  # maybe remove all the seeds after
  mv "$qcow" "$qcows_vms_prefix/$qcow"
  mv "$seed" "$qcows_vms_prefix/$seed"
  chown -R libvirt-qemu:kvm "$qcows_vms_prefix/$seed" # /var/lib/libvirt/images/qcows/vms-ub
  chown -R libvirt-qemu:kvm "$qcows_vms_prefix/$qcow" # /var/lib/libvirt/images/qcows/vms-ub

}
createqcows (){
  echo "${ub_names[*]}"
  for VM_NAME in "${ub_names[@]}"
    do
     :
      createqcow "$VM_NAME"

  done
}
install_vm (){
  vmn=$1
  qcow="$qcows_vms_prefix/$vmn.qcow2" # qcow before img
  seed="$qcows_vms_prefix/$vmn.seed.img"
  virt-install --name="$vmn" --ram="$RAM" --vcpus="$VCPUS" --import \
    --disk path="$qcow",format=qcow2 \
    --disk path="$seed",device=cdrom \
    --os-variant="$OS_VARIANT" \
    --network type=network,source=default,model=virtio \
    --graphics vnc,listen=0.0.0.0 --noautoconsole

#  virt-install --name=hal9000 --ram=2048 --vcpus=2 --import \
#    --disk path=/var/lib/libvirt/images/vm/hal9000/hal9000.qcow2,format=qcow2 \
#    --disk path=/var/lib/libvirt/images/vm/hal9000/seed.img,device=cdrom \
#    --os-variant=ubuntu20.04 \
#    --network type=network,source=default,model=virtio \
#    --graphics vnc,listen=0.0.0.0 --noautoconsole
}
install_vms () {
  for VM_NAME in "${ub_names[@]}"
    do
     :
      echo Creating "$VM_Name"
      install_vm "$VM_NAME" # maybe add delay...

  done
}


# Main

check_user_data_schema
check_range # this has to be ran

main_all () {
  # install_packages # 1.
#  install_packages
  initialize_folder_structure # 2.
  check_base_img_or_download # 3.
  # 4. create qcows
  createqcows
  ##createqcow ub1
  # 5. Install all vms
  install_vms
  ##install_vm ub1

}
#main_all
print_network # should add static macs?
#ssh_into_vm ub1
#dev_delete_images

#


#print_network
#ssh_into_vm ub1
