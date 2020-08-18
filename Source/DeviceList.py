#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 18-08-2020 07.41.41
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True

import os
import subprocess, shlex
import json
from  types import SimpleNamespace


# ###########################################################################
# # set logger and color
# ###########################################################################
def setup(gVars):
    global C, logger
    if 'color' in gVars: C=gVars['color']
    if 'logger' in gVars: logger=gVars['logger']


# ###########################################################################
# # esegue il comando blkid
# # Esempio di riga:
# #   /dev/sdb5: LABEL="Lacie232GB_A" UUID="1448564A48562AAE" TYPE="ntfs"
# # It is recommended to use
# #       lsblk(8) command to get information about block devices,
# #    or lsblk --fs to get an overview of filesystems,
# #    or findmnt(8) to search in already mounted filesystems.
# # lsblk --help per avere la lista dei campi di output
# # lsblk --json -o NAME,FSTYPE,LABEL,UUID,MOUNTPOINT,PARTUUID,SIZE,PATH
# ###########################################################################
def deviceList(uuids):
    # ----- get list of BLK_DEVICES
    CMD='/bin/lsblk --json --sort NAME -o NAME,FSTYPE,LABEL,UUID,MOUNTPOINT,PARTUUID,SIZE,PATH'
    dev_list = subprocess.check_output(shlex.split(CMD))
    blk_devices = json.loads(dev_list)["blockdevices"] # list of dict
    logger.info('DEVICES', json.dumps(blk_devices, indent=4, sort_keys=True))


    '''
        cut no fstype and system devices (mmcblk0..)
        merge with configuration data
    '''
    found_DEVICES={}
    for item in blk_devices:
        _device=SimpleNamespace(**item) #  just for easy management

        if _device.fstype and not _device.name.startswith('mmcblk0'):
            if _device.mountpoint: # if already mounted
                _device.mounted=True
                _device.mp_dynamic=False

            elif _device.uuid in uuids:
                _device.mounted=False
                _device.mp_dynamic=False
                #- copy from configuration file
                _device.mountpoint=uuids[_device.uuid]['mountpoint']
            else:
                _device.mounted=False
                _device.mp_dynamic=True
                #- create dynamic mp
                _device.mountpoint=f'/mnt/{_device.label}-{_device.partuuid}'

            found_DEVICES[_device.name]=_device.__dict__ # put dict version

    logger.info('DEVICES found:', found_DEVICES)
    return found_DEVICES
