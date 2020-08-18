#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 18-08-2020 09.02.42
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
from pathlib import Path
from types import SimpleNamespace
import subprocess, shlex

from LnLib.promptLN import prompt
from LnLib.nameSpaceLN import RecursiveNamespace
from LnLib.localExec import runCommand

# ###########################################################################
# #
# ###########################################################################
def setup(gVars={}):
    if gVars:
        global C, logger
        if 'color' in gVars: C=gVars['color']
        if 'logger' in gVars: logger=gVars['logger']


# ###########################################################################
# #
# ###########################################################################
def mount(dev, fEXECUTE=False):
    assert isinstance(dev, dict)
    dev=SimpleNamespace(**dev)

    if dev.mounted:
        logger.console(f"device {dev.path} already mounted: {dev.mountpoint}")
        return 0

    C.pWhiteH(text="trying to mount disk {dev.path}".format(**locals()), tab=4)
    if dev.fstype=='vfat':
        OPTIONS='-o defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
    elif dev.fstype=='ntfs':
        OPTIONS='-o defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
    else:
        OPTIONS=''

    CMD="sudo /bin/mount -t {dev.fstype} {OPTIONS} -U {dev.uuid} {dev.mountpoint}".format(**locals())
    C.pYellowH(text=CMD, tab=4)

    if not fEXECUTE:
        print()
        choice=prompt('    Enter "go" to proceed with mount.', validKeys='go')
        if choice.lower()=='go':
            fEXECUTE=True

    if fEXECUTE:
        check_mp(dev.mountpoint)
        result=subprocess.check_output(shlex.split(CMD))
        if result:
            msg="ERRORE nell'esecuzione del comando di mount"
            C.pError(text=msg, tab=4)
            logger.critical(msg)
        else:
            logger.info(f'device {dev.path} has been mounted on dir: {dev.mountpoint}')

    return 0


# ###########################################################################
# #
# ###########################################################################
def umount(dev, fEXECUTE=False):
    assert isinstance(dev, dict)
    dev=SimpleNamespace(**dev)

    if not dev.mounted:
        logger.console(f"device {dev.path} not mounted.")
        return


    umount_cmd=f"sudo /bin/umount {dev.mountpoint}"
    C.pYellowH(text=umount_cmd, tab=4)

    if not fEXECUTE:
        print()
        choice=prompt('    Enter "go" to proceed with umount.', validKeys='go')
        if choice.lower()=='go':
            fEXECUTE=True

    if fEXECUTE:
        rCode, result=runCommand(umount_cmd, logger)
        if rCode:
            logger.critical("ERRORE nell'esecuzione del comando", umount_cmd)
        else:
            rCode, result=runCommand(f'sudo rm -rf {dev.mountpoint}', logger)
            C.pYellowH(f'mountpoint directory removing - rCode: {rCode}', tab=4)

    return 0

##################################################
# check mount-point
##################################################
def check_mp(mountpoint):

    logger.info('creating mount-point:', mountpoint)
    if not Path(mountpoint).is_dir():
        C.pCyan(f"mountpoint directory {mountpoint} doesn't exists... creating it.", tab=4)

        rCode, out=runCommand(f'sudo mkdir {mountpoint}', logger)
        if rCode:
            msg=f"Error creating directory: {mountpoint}"
            C.pError(msg, tab=4)
            logger.critical(msg)
        else:
            C.pYellowH(text="directory has been created", tab=4)

        rCode, out=runCommand(f'sudo chown pi:pi {mountpoint}', logger)
        if rCode:
            msg=f"Error during chown on direcory: {mountpoint}"
            C.pError(msg, tab=4)
            logger.critical(msg)
        else:
            C.pYellowH("directory owner has been changed", tab=4)
    else:
        logger.info('   directory already exists.')
