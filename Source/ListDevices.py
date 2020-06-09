#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 07-06-2020 13.45.12
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True

import os
import subprocess
import json
# import string # per maketrans
from LnLib.LnPyUtils import stringSplitRE

# ###########################################################################
# # esegue il comando blkid
# # Esempio di riga:
# #   /dev/sdb5: LABEL="Lacie232GB_A" UUID="1448564A48562AAE" TYPE="ntfs"
# ###########################################################################
def getBlockID(gv, reqUUID=None):
    logger=gv.lnLogger

    # contiene la lista dei device ricavati dai comandi: mount (oppure df) e da blkid
    DEVICES = {}
    PARTUUID = {}


    dev_list = subprocess.check_output('/sbin/blkid', stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
    dev_list = dev_list.decode('utf-8')       # converti in STRing

    '''
        /dev/mmcblk0p1: LABEL="boot" UUID="DDAB-3A15" TYPE="vfat" PARTUUID="7b28d388-01"
        /dev/mmcblk0p2: LABEL="rootfs" UUID="5fa1ec37-3719-4b25-be14-1f7d29135a13" TYPE="ext4" PARTUUID="7b28d388-02"
        /dev/sda1: LABEL="TOSHIBA EXT" UUID="843671A53671993E" TYPE="ntfs" PARTUUID="7fcb449d-01"
        /dev/sda2: UUID="441d4b2e-2e17-451d-8835-485e388f6595" TYPE="ext4" PARTUUID="7fcb449d-02"
    '''
    for line in dev_list.split('\n'):
        if not line: continue   # se vuota loop
        logger.info(line, console=True)

        _data=stringSplitRE(line, delimiters=(':', '=', '"'))

        device_name=_data[0]
        if device_name.startswith('/dev/mmcblk0'): # Skip Raspberry SD device
            logger.info('skipping device:', device_name)
            continue

        if not device_name in DEVICES.keys():
            DEVICES[device_name] = {
                'uuid': '',
                'partuuid': '',
                'label': '',
                'type': '',
            }
            ptr=DEVICES[device_name]
            logger.info('adding device:', device_name)

        for index, item in enumerate(_data):
            if item=='UUID':
                ptr['uuid']=_data[index+1]
            elif item=='PARTUUID':
                ptr['partuuid']=_data[index+1]
            elif item=='LABEL':
                ptr['label']=_data[index+1]
            elif item=='TYPE':
                ptr['type']=_data[index+1]

        if ptr['partuuid']:
            PARTUUID[ptr['partuuid']]={
                'uuid': ptr['uuid'],
                'device_name': device_name,
                'label': ptr['label'],
                'type': ptr['type'],
            }

        '''
            nel caso volessi maggiori dettagli potrei usar il comando:
            CMD = 'sudo /sbin/blkid -o udev -p ' + device_name
            resBytes = subprocess.check_output( CMD.split() ) #  per usare il sudo
            resList = resBytes.decode('utf-8').split('\n')       # converti in STRing/LIST
        '''
    logger.info('DEVICES', json.dumps(DEVICES, indent=4, sort_keys=True))
    logger.info('PARTUUID', json.dumps(PARTUUID, indent=4, sort_keys=True))
    return DEVICES




def getBlockID_prev(gv, reqUUID=None):
    logger=gv.logger

    # contiene la lista dei device ricavati dai comandi: mount (oppure df) e da blkid
    DEVICES = {}


    blockDev = subprocess.check_output('/sbin/blkid', stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
    blockDev = blockDev.decode('utf-8')       # converti in STRing

    """
        *** ho riscontrato la non veridicità sui dati della riga del blkid.
        *** Ho scoperto che è meglio interrograre uno per uno i device
    for line in res.split('\n'):
        logger.info(line)
        if not line: continue   # se vuota loop
        devName, rest = line.split(':')                         # prendi nome device ...
        if not devName in DEVICES: DEVICES[devName] = {}    # creiamo l'entry, se non esiste
        vals = rest.split()                                     # la parte restante la spezziamo
        logger.info('adding device: ' + devName)
        for val in vals:
            name, value = val.split('=')
            DEVICES[devName][name] = value.strip('"')
    """


    for line in blockDev.split('\n'):
        if not line: continue   # se vuota loop
        logger.info(line, console=True)
        devName, rest = line.split(':')                         # prendi nome device ... rest lo ignoriamo perché ritenuto non valido

           # Skip dei device della scheda SD del RaspBerry
        if devName.startswith('/dev/mmcblk0'):
            logger.info('skipping device: ' + devName + '\n')
            continue

        if not devName in DEVICES.keys():
            DEVICES[devName] = {}
            logger.info('adding device: ' + devName)
        else:
            logger.info('modifying device: ' + devName)


        CMD = 'sudo /sbin/blkid -o udev -p ' + devName
        resBytes = subprocess.check_output( CMD.split() ) #  per usare il sudo
        resList = resBytes.decode('utf-8').split('\n')       # converti in STRing/LIST

        # if not devName in DEVICES.keys(): DEVICES[devName] = {}    # creiamo l'entry
        for line in resList:
            if not line: continue   # se vuota loop
            logger.info ('    ' + line)
            name, value = line.split('=')
            DEVICES[devName][name] = value.strip('"')            # xx = binary_to_dict(result)
        logger.info ('')

        print(json.dumps(DEVICES, indent=4, sort_keys=True))

def ListDevices(gv):
    gv.BLKID = getBlockID()
    gv.FS    = getMountedFS('/mnt/')


if __name__ == "__main__":
    global gv
    gv = LnClass()