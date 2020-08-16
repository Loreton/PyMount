#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 16-08-2020 13.46.52
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
from pathlib import Path
from types import SimpleNamespace
import subprocess, shlex

from LnLib.promptLN import prompt
from LnLib.nameSpaceLN import RecursiveNamespace


# ###########################################################################
# #
# ###########################################################################
def mountDevice(dev, fEXECUTE=False, gVars={}):
    assert isinstance(dev, dict)
    if gVars:
        global C
        if 'color' in gVars: C=gVars['color']

    dev=SimpleNamespace(**dev)

    if dev.mounted:
        print("device already mounted")
        return

    elif Path(dev.mountpoint).is_dir():
        C.pWhiteH(text="trying to mount disk {dev.path}".format(**locals()), tab=8)
        if dev.fstype=='vfat':
            OPTIONS='-o defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
        elif dev.fstype=='ntfs':
            OPTIONS='-o defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
        else:
            OPTIONS=''

        CMD="sudo /bin/mount -t {dev.fstype} {OPTIONS} -U {dev.uuid} {dev.mountpoint}".format(**locals())
        C.pYellowH(text=CMD, tab=8)

        if not fEXECUTE:
            print()
            choice=prompt('    Enter "go" to proceed with mount.', validKeys='go')
            if choice.lower()=='go':
                fEXECUTE=True

        if fEXECUTE:
            result=subprocess.check_output(shlex.split(CMD))
            if result:
                C.pError(text="ERRORE nell'esecuzione del comando di mount", tab=8)

    else:
        C.pYellowH(text="""
            mountpoint directory doesn't exists.
            Please create it.
            """, tab=4)
        sys.exit(1)

