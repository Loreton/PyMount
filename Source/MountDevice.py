#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 09-06-2020 19.30.30
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
import subprocess

# ###########################################################################
# #
# ###########################################################################
def MountDevice(gv, req_device):
    logger=gv.lnLogger
    C=gv.Color


    for device, data in device_list.items():
        C.yellowH(text=device, tab=4)
        if 'label' in data:     C.cyanH(text='{:12}: {}'.format('LABEL', data.label), tab=8)
        if 'uuid' in data:      C.cyanH(text='{:12}: {}'.format('UUID', data.uuid), tab=8)
        if 'partuuid' in data:  C.cyanH(text='{:12}: {}'.format('PARTUUID', data.partuuid), tab=8)
        if 'size' in data:      C.cyanH(text='{:12}: {}'.format('SIZE', data.size), tab=8)
        if 'fstype' in data:    C.cyanH(text='{:12}: {}'.format('FSTYPE', data.fstype), tab=8)
        if 'mount_point' in data:    C.magentaH(text='{:12}: {}'.format('mount_point', data.mount_point), tab=8)
        print()

    if not device_found:
        print()