# Quicky stop and recopy vm - as admin
# i feel like this is rather slow
# don't need python for this
stop-vm ub1
copy "G:\HyperVImages\vms\ub1\Virtual Hard Disks\ub1_bak.vhdx" "G:\HyperVImages\vms\ub1\Virtual Hard Disks\ub1.vhdx"
start-vm ub1