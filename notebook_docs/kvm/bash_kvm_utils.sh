# bash alias / functions
# maybe look into bash completion as well?
# exec bash -l
# restarts bash
alias jc_vkvm_net_dhcp_leases_default="virsh net-dhcp-leases default"
# unalias
# unset -f fnname

res___get_kvm_ip=''
__get_kvm_ip () {
  local vmn=${1:-ub1}
  res___get_kvm_ip=$(virsh domifaddr "$vmn" | awk '/ipv4/ {print $4}' | awk -F'/' '{print $1}')
  return 0
}
jc_vkvm_debug_guest () {
  local vmn=${1:-ub1}
  echo "--- Lookup Guest: $vmn ---"
  local virsh_list_all=$(virsh list --all)
  grep -i -a1 State <<< "$virsh_list_all" # get first two lines of starting table
  grep "$vmn" <<< "$virsh_list_all" # grep ub1 <<< "$virsh_list_all"
  virsh net-dhcp-leases default
  echo "--- Lookup IP: $vmn ---"
  __get_kvm_ip "$vmn"
  echo "$res___get_kvm_ip"

}
# jc_kvm_debug_guest

jc_ssh_vm_lnx () {
  local vmn=${1:-ub1}
  # local vmu=${2:-root}
  local vmu=${2:-jason}
  __get_kvm_ip "$vmn"
  local ssh_cmd="ssh $vmu@$res___get_kvm_ip" # maybe echo as well?
  echo "ssh cmd fir guest: $vmn"
  echo "$ssh_cmd"
  $($ssh_cmd)

  
}
# jc_ssh_vm_lnx ub1 jason
# ssh root@localhost

# ssh Administrator@`virsh domifaddr win2k19 | awk '/ipv4/ {print $4}' | awk -F'/' '{print $1}'`
# virsh net-dumpxml default
# virsh list --all


check_ssh_config () {
  cat /etc/ssh/sshd_config
  cp /etc/ssh/sshd_config .
  # better way is to check for 
  # Include /etc/ssh/sshd_config.d/*.conf
  # and put that stuff there. since it's system wide

}
# check_ssh_config

# https://unix.stackexchange.com/questions/453585/shell-script-to-comment-and-uncomment-a-line-in-file
__comment() {
    local regex="${1:?}"
    local file="${2:?}"
    local comment_mark="${3:-#}"
    sed -ri "s:^([ ]*)($regex):\\1$comment_mark\\2:" "$file"
}

__uncomment() {
    # __uncomment "PubkeyAuthentication" sshd_config
    # __uncomment "PubkeyAuthentication" sshd_config
    local regex="${1:?}"
    local file="${2:?}"
    local comment_mark="${3:-#}"
    sed -ri "s:^([ ]*)[$comment_mark]+[ ]?([ ]*$regex):\\1\\2:" "$file"
}
#  __uncomment "PubkeyAuthentication" /etc/ssh/sshd_config
# service sshd restart
# ssh root@localhost # something wrong with settings on the guest
# maybe a bit better
# echo "PubkeyAuthentication yes" > /etc/ssh/sshd_config.d/jc-init.conf
# service sshd restart
# need to look at cloud init sshd_config files...