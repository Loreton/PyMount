#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 10-06-2020 16.40.12
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
from pathlib import Path
from dotmap import DotMap
import subprocess

# ###########################################################################
# #
# ###########################################################################
def MountDevice(gv, dev):
    logger=gv.lnLogger
    C=gv.Color
    config=gv.config

    dev=DotMap(dev, _dynamic=False)

    if dev.mounted:
        print("device already mounted")
        sys.exit()

    elif Path(dev.mountpoint).is_dir():
        print("trying to mount disk {dev.path}".format(**locals()))
        if dev.fstype=='vfat':
            OPTIONS='-o defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
        elif dev.fstype=='ntfs':
            OPTIONS='-o defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
        else:
            OPTIONS=''

        CMD="sudo /bin/mount -t {dev.fstype} {OPTIONS} -U {dev.uuid} {dev.mountpoint}".format(**locals())
        print (CMD)
        result=subprocess.check_output(CMD.split())
        print(result)

    else:
        C.yellowH(text="""
            mountpoint directory doesn't exists.
            Please create it.
            """, tab=4)
        sys.exit(1)

