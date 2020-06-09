#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 09-06-2020 19.29.21
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
import subprocess

# ###########################################################################
# #
# ###########################################################################
def CheckDevices(gv, device_list, req_device=None, req_partuuid=None, req_uuid=None):
    logger=gv.lnLogger
    C=gv.Color


    device_found={}
    for device, data in device_list.items():
        if (req_device) and (device==req_device):
            device_found[device]=device_list.pop(device)
            break
        elif (req_partuuid) and ('partuuid' in data) and (data.partuuid==req_partuuid):
            device_found[device]=device_list.pop(device)
            break
        elif (req_uuid) and ('uuid' in data) and (data.uuid==req_uuid):
            device_found[device]=device_list.pop(device)
            break

    if device_found:
        device_list=device_found

    for device, data in device_list.items():
        C.yellowH(text=device, tab=4)
        if 'label' in data:     C.cyanH(text='{:12}: {}'.format('LABEL', data.label), tab=8)
        if 'uuid' in data:      C.cyanH(text='{:12}: {}'.format('UUID', data.uuid), tab=8)
        if 'partuuid' in data:  C.cyanH(text='{:12}: {}'.format('PARTUUID', data.partuuid), tab=8)
        if 'size' in data:      C.cyanH(text='{:12}: {}'.format('SIZE', data.size), tab=8)
        if 'fstype' in data:    C.cyanH(text='{:12}: {}'.format('FSTYPE', data.fstype), tab=8)
        if 'mount_point' in data:    C.magentaH(text='{:12}: {}'.format('mount_point', data.mount_point), tab=8)
        print()

    return device_found