# PyTest
import sys
import pytest
import logging as log

import subprocess
# G:\HyperVImages\vms\ub1\Virtual Hard Disks
# G:\HyperVImages\vms\ub1\Virtual Hard Disks\ub1.vhdx
# "G:\HyperVImages\vms\ub2204-server-min-g2_archive\ub2204-server-min-g2.vhdx"
# https://www.phillipsj.net/posts/executing-powershell-from-python/
# https://learn.microsoft.com/en-us/powershell/module/hyper-v/stop-vm?view=windowsserver2022-ps
"""

need to be admin
stop-vm ub1
WARNING: The virtual machine is already in the specified state.

Start-VM ub1
"""
def run_ps1(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed



def test_name():
    log.warning("hi")


if __name__ == '__main__':
    pytest.main(sys.argv)
