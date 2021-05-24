#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 24-09-2020 14.48.10
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True

import os
import subprocess, shlex
import json
import DisplayDevice


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
def lsblk():
    # ----- get list of BLK_DEVICES
    CMD='/bin/lsblk --json --sort NAME -o NAME,FSTYPE,LABEL,UUID,MOUNTPOINT,PARTUUID,SIZE,PATH'
    dev_list=subprocess.check_output(shlex.split(CMD))
    lk_devices=json.loads(dev_list)["blockdevices"] # list of dict
    return lk_devices


# ###########################################################################
# #
# ###########################################################################
def processDevice(device: dict, cfg_device: dict=None):
    uuid=device['uuid']
    if device['fstype'] is None or device['name'].startswith('mmcblk0') or uuid is None:
        return None

    elif device['mountpoint']: # if already mounted
        device['mounted']=True
        device['dynamic_mp']=False

    elif cfg_device.get('mountpoint'): # present in configuration
        device['mounted']=False # default
        device['dynamic_mp']=False # default
        device['mountpoint']=cfg_device['mountpoint'] # get from configuration file

    else:
        device['mountpoint']=f"/mnt/{device['label']}-{device['partuuid']}" #-  dynamic mountpoint

    return device # modified device




# ###########################################################################
# # return all available devices
# ###########################################################################
def deviceList(config, myLogger, fPRINT=False):
    global logger
    logger=myLogger

    lk_devices=lsblk()
    logger.debug('system devices:', lk_devices)

    device_list={}
    for device in lk_devices:
        logger.info('processing:', device)
        ret=processDevice(device, cfg_device=config.get(device['uuid']))
        if ret:
            logger.info('   valid')
            dev_name=ret['name']
            device_list[dev_name]=ret
        else:
            logger.info('   skipped')

    logger.debug('valid devices:', device_list)
    if fPRINT:
        for name, device in device_list.items():
            DisplayDevice.display(device, msg='current status')
        print()
    return device_list



# ###########################################################################
# #
# ###########################################################################
def getDevice(config, myLogger, **kwargs):
    device_list=deviceList(config=config, myLogger=myLogger, fPRINT=False)

    for name, device in device_list.items():
        if name==kwargs.get('name') or device['uuid']==kwargs.get('uuid') or device['partuuid']==kwargs.get('partuuid') or device['label']==kwargs.get('label'):
            logger.info('DEVICE found:', device)
            return device

    logger.warning('NO DEVICE found:')
    return None
