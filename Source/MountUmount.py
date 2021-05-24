#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 24-09-2020 15.13.34
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
from pathlib import Path
from types import SimpleNamespace
import subprocess, shlex


from colorLN import LnColor; C=LnColor()

# from LnLib.promptLN import prompt
# from LnLib.nameSpaceLN import RecursiveNamespace
from runCommandLN import runCommand

# # ###########################################################################
# # #
# # ###########################################################################
# def setup(gVars={}):
#     if gVars:
#         global C, logger
#         if 'color' in gVars: C=gVars['color']
#         if 'logger' in gVars: logger=gVars['logger']


# ###########################################################################
# # return: 0 all is OK
# ###########################################################################
def mount(dev, *, my_logger, fEXECUTE=False):
    global logger
    logger=my_logger
    assert isinstance(dev, dict)
    logger.info('DEVICE required:', dev)
    dev=SimpleNamespace(**dev)

    if dev.mounted:
        msg = f"device {dev.path} already mounted: {dev.mountpoint}"
        logger.info(msg)
        C.pYellowH(text=msg, tab=4)
        return 0

    C.pWhiteH(text=f"trying to mount disk {dev.path}", tab=4)
    if dev.fstype=='vfat':
        OPTIONS='-o defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
    elif dev.fstype=='ntfs':
        OPTIONS='-o defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
    else:
        OPTIONS=''

    mount_cmd=f"sudo /bin/mount -t {dev.fstype} {OPTIONS} -U {dev.uuid} {dev.mountpoint}"


    if fEXECUTE:
        C.pYellowH(text=mount_cmd, tab=4)
        check_mp(dev.mountpoint)
        # result=subprocess.check_output(shlex.split(mount_cmd))
        rCode, result=runCommand(mount_cmd, logger)
        if result:
            msg="ERRORE nell'esecuzione del comando di mount"
            C.pError(text=msg, tab=4)
            logger.critical(msg)
        else:
            msg=f'device {dev.path} has been mounted on dir: {dev.mountpoint}'
            logger.info(msg)
            C.pCyanH(text=msg, tab=4)

    else:
        C.pYellowH(text=f'DRY-RUN - {mount_cmd}', tab=4)
        rCode=0

    return rCode


# ###########################################################################
# #
# ###########################################################################
def umount(dev, *, my_logger, fEXECUTE=False):
    global logger
    logger=my_logger

    assert isinstance(dev, dict)
    logger.info('DEVICE required:', dev)
    dev=SimpleNamespace(**dev)

    if not dev.mounted:
        msg=f"device {dev.path} not mounted."
        logger.info(msg)
        C.pYellowH(text=msg, tab=4)
        return 0


    umount_cmd=f"sudo /bin/umount {dev.path}"

    if fEXECUTE:
        C.pYellowH(text=umount_cmd, tab=4)
        rCode, result=runCommand(umount_cmd, logger)
        if rCode:
            msg=f"ERRORE nell'esecuzione del comando {umount_cmd}"
            C.pError(text=msg, tab=4)
            logger.critical("ERRORE nell'esecuzione del comando", umount_cmd)
        else:
            rCode1, result=runCommand(f'sudo rm -rf {dev.mountpoint}', logger)
            C.pYellowH(f'mountpoint directory removing - rCode: {rCode1}', tab=4)
    else:
        C.pYellowH(text=f'DRY-RUN - {umount_cmd}', tab=4)
        rCode=0

    return rCode

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

