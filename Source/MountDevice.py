#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 15-08-2020 17.09.11
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
from pathlib import Path
# from dotmap import DotMap
import subprocess

from LnLib.promptLN import prompt
from LnLib.nameSpaceLN import RecursiveNamespace


##########################################################
#
##########################################################
class nullLogger():
    def dummy(self,  title, *args, **kwargs): pass
    critical=error=warning=info=debug=debug1=debug2=debug3=set_level=dummy


# ###########################################################################
# #
# ###########################################################################
def MountDevice(dev, fEXECUTE=False, logger=nullLogger()):
    dev=RecursiveNamespace(dev.__dict__)

    if dev.mounted:
        print("device already mounted")
        sys.exit()

    elif Path(dev.mountpoint).is_dir():
        C.whiteH(text="trying to mount disk {dev.path}".format(**locals()), tab=8)
        if dev.fstype=='vfat':
            OPTIONS='-o defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
        elif dev.fstype=='ntfs':
            OPTIONS='-o defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
        else:
            OPTIONS=''

        CMD="sudo /bin/mount -t {dev.fstype} {OPTIONS} -U {dev.uuid} {dev.mountpoint}".format(**locals())
        C.yellowH(text=CMD, tab=8)

        if not fEXECUTE:
            print()
            choice=prompt('    Enter "go" to proceed with mount.', validKeys='go')
            if choice.lower()=='go':
                fEXECUTE=True

        if fEXECUTE:
            result=subprocess.check_output(CMD.split())
            if result:
                C.error(text="ERRORE nell'esecuzione del comando di mount", tab=8)

    else:
        C.yellowH(text="""
            mountpoint directory doesn't exists.
            Please create it.
            """, tab=4)
        sys.exit(1)

