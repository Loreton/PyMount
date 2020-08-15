#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 15-08-2020 19.01.03
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True

import os
import subprocess, shlex
import json
from  types import SimpleNamespace

from LnLib.nameSpaceLN import RecursiveNamespace
from LnLib.splitStringLN import stringSplitRE
from LnLib.bytesToHumanLN import bytes2H


def _set(Color)
    gobal C
    C=Color()


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
def DeviceList(uuids, logger):
    # logger=gv.lnLogger
    # config_dev=gv.config.UUID

    # ----- list of BLK_DEVICES
    CMD='/bin/lsblk --json --sort NAME -o NAME,FSTYPE,LABEL,UUID,MOUNTPOINT,PARTUUID,SIZE,PATH'
    dev_list = subprocess.check_output(shlex.split(CMD))
    blk_devices = json.loads(dev_list)["blockdevices"] # list of dict
    logger.info('DEVICES', json.dumps(blk_devices, indent=4, sort_keys=True))


    # ----- cut no fstype and system devices (mmcblk0..)
    DEVICES={}
    for item in blk_devices:
        item=SimpleNamespace(**item) #  just for easy mnagement
        # item=RecursiveNamespace(**item) #  just for easy mnagement
        if item.fstype and not item.name.startswith('XXXXXX_mmcblk0'):
            if not item.mountpoint:
                item.mounted=False
                    # copiamolo dal file di configurazione
                if item.uuid in uuids:
                    item.mountpoint=uuids[item.uuid]['mountpoint']
            else:
                item.mounted=True
            DEVICES[item.name]=item.__dict__ # put dict version



    # logger.info('DEVICES', json.dumps(DEVICES, indent=4, sort_keys=True))
    print(type(DEVICES))
    logger.info('DEVICES found:', DEVICES)
    return DEVICES
