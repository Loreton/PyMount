#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 10-06-2020 15.59.26
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True

import os
import subprocess
import json
from dotmap import DotMap

# import string # per maketrans
from LnLib.LnPyUtils import stringSplitRE
from LnLib.LnPyUtils import bytes2H

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
def DeviceList(gv, reqUUID=None):
    logger=gv.lnLogger
    config_dev=gv.config.UUID

    CMD='/bin/lsblk --json --sort NAME -o NAME,FSTYPE,LABEL,UUID,MOUNTPOINT,PARTUUID,SIZE,PATH'
    dev_list = subprocess.check_output(CMD.split())
    my_dict = DotMap(json.loads(dev_list), _dynamic=False)
    logger.info('DEVICES', json.dumps(my_dict, indent=4, sort_keys=True))

    # - Elimina le non partitions ed i device di sistema
    DEVICES={}
    for item in my_dict["blockdevices"]:
        if item.fstype and not item.name.startswith('xxmmcblk0'):
            if not item.mountpoint:
                item.mounted=False
                    # copiamolo dal file di configurazione
                if item.uuid in config_dev:
                    item.mountpoint=config_dev[item.uuid]['mountpoint']
            else:
                item.mounted=True
            DEVICES[item.name]=item



    logger.info('DEVICES', json.dumps(DEVICES, indent=4, sort_keys=True))
    return DotMap(DEVICES, _dynamic=False)

# ###########################################################################
# # esegue il comando blkid
# # Esempio di riga:
# #   /dev/sdb5: LABEL="Lacie232GB_A" UUID="1448564A48562AAE" TYPE="ntfs"
# ###########################################################################
def DeviceList_(gv, reqUUID=None):
    logger=gv.lnLogger

    # contiene la lista dei device ricavati dai comandi: mount (oppure df) e da blkid
    # DEVICES = {}
    DEVICES = DotMap(_dynamic=False)


    ''' blkid sample output command
        /dev/mmcblk0p1: LABEL="boot" UUID="DDAB-3A15" TYPE="vfat" PARTUUID="7b28d388-01"
        /dev/mmcblk0p2: LABEL="rootfs" UUID="5fa1ec37-3719-4b25-be14-1f7d29135a13" TYPE="ext4" PARTUUID="7b28d388-02"
        /dev/sda1: LABEL="TOSHIBA EXT" UUID="843671A53671993E" TYPE="ntfs" PARTUUID="7fcb449d-01"
        /dev/sda2: UUID="441d4b2e-2e17-451d-8835-485e388f6595" TYPE="ext4" PARTUUID="7fcb449d-02"
    '''
    dev_list = subprocess.check_output('/sbin/blkid', stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
    dev_list = dev_list.decode('utf-8')       # converti in STRing

    for line in dev_list.split('\n'):
        if not line: continue   # se vuota loop
        logger.info('line:', line)
        device_name=line.split(':')[0]
        logger.info('working on device:', device_name)
        if device_name.startswith('/dxev/mmcblk0'): # Skip Raspberry SD device
            logger.info('   ...skipping device')
            continue

        # - lo lascio solo come esempio
        _data=stringSplitRE(line, delimiters=(':', '=', '"'))


        CMD = 'sudo /sbin/blkid -o udev -p ' + device_name
        resBytes = subprocess.check_output( CMD.split() ) #  per usare il sudo
        device_data = resBytes.decode('utf-8').split('\n')    # converti in STRing/LIST
        logger.info('device_data:', device_data)

        ptr=DEVICES[device_name]=DotMap(_dynamic=False)
        for item in device_data:
            if not item: continue
            name, value = item.split('=')
            if name=='ID_FS_LABEL':
                ptr['label']=value
            if name=='ID_FS_UUID':
                ptr['uuid']=value
            if name=='ID_FS_TYPE':
                ptr['fstype']=value
            if name=='ID_PART_ENTRY_UUID':
                ptr['partuuid']=value
            if name=='ID_PART_ENTRY_SIZE':
                ptr['size']=bytes2H(int(value))


    mounted = subprocess.check_output('/bin/mount', stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
    mounted = mounted.decode('utf-8').split('\n')       # converti in STRing/LIST


    for item in mounted:
        if not item.strip(): continue
        dev_name, _, mount_point,_ = item.split(' ', 3)
        for device in DEVICES.keys():
            if device==dev_name:
                DEVICES[device]['mount_point']= mount_point


    logger.info('DEVICES', json.dumps(DEVICES, indent=4, sort_keys=True))
    return DEVICES
