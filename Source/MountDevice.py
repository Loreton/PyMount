#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 17-08-2020 15.58.12
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
        global C, logger
        if 'color' in gVars: C=gVars['color']
        if 'logger' in gVars: logger=gVars['logger']

    dev=SimpleNamespace(**dev)

    if dev.mounted:
        print("device already mounted")
        return

    elif not Path(dev.mountpoint).is_dir():
        C.pYellowH(f"""
            mountpoint directory {dev.mountpoint} doesn't exists.
            I'm going to create it.
            """, tab=4)

        rCode, out=localExec(f'sudo mkdir {dev.mountpoint}')
        if rCode:
            C.pError("Errore nella creazione delle directory", tab=4)
            sys.exit(1)

        rCode, out=localExec(f'sudo chown pi:pi {dev.mountpoint}')
        if rCode:
            C.pError("Errore durante il chown", tab=4)
            sys.exit(1)


    if Path(dev.mountpoint).is_dir():
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
            shoud not occurr. !!!!????
            """, tab=4)
        sys.exit(1)




##################################################
# _alias_exec
##################################################
def localExec(command):
    splitted_cmd=shlex.split(command)
    logger.debug1('executing command:', [command])

    try:
        p1 = subprocess.run(splitted_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, check=True)
        logger.debug3('    rcode: ', p1.returncode)
        logger.debug3('    result:', p1.stdout)
        return p1.returncode, p1.stdout

    except subprocess.CalledProcessError as e:
        logger.error("ERROR:", "",
                          f"command:   {command}",
                          f"rcode:     {e.returncode}",
                          f"exception: {str(e)}")

        return e.returncode, str(e)