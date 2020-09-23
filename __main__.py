#!/usr/local/bin/python3
# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 23-09-2020 18.47.43
#
# #############################################

import sys; sys.dont_write_bytecode = True
import os
from   pathlib import Path
from types import SimpleNamespace
import pdb

##############################################################################
# - classe utile da passare per moduli che richiedo il logger.
##############################################################################
class nullLogger():
    def dummy(self,  title, *args, **kwargs): pass
    critical=error=warning=info=debug=debug1=debug2=debug3=set_level=dummy
from LnLib.colorLN import LnColor; C=LnColor()
_myGlobalInitialSettings={'logger': nullLogger(), 'color': LnColor()}


import types # for SimpleNamespace()

from LnLib.yamlLoaderLN import loadYamlFile
from LnLib.loggerLN     import setLogger
from LnLib.promptLN     import prompt
from LnLib              import monkeyPathLN # necessario per i miei comandi di Path (tra cui file.sizeRotate())


from Source.parseInputLN import parseInput
from Source import DeviceList
from Source import MountUmount
from Source import DisplayDevice; display=DisplayDevice.display

######################################
# sample call:
#
######################################
if __name__ == '__main__':
    gv=types.SimpleNamespace()

    prj_dir=Path(sys.argv[0]).resolve().parent

    '''
        Questo step serve per quando siamo all'interno dello zip
        anche se, per non incorrere in errori,
        mi conviene impostare il nome staticamente
    '''
    if prj_dir.stem=='bin': prj_dir=prj_dir.parent
    prj_name=prj_dir.stem
    prj_name='pymount'

    os.environ['Prj_Name']=prj_name # potrebbe usarla loadYamlFile()

    ''' read Main configuration file '''
    dConfig=loadYamlFile(f'conf/{prj_name}.yml', resolve=True, fPRINT=False)

    ''' parsing input (return Namespace data)'''
    args, inp_log, dbg=parseInput(color=C)

    ''' logger '''
    log=dConfig['logger']
    log['filename']=f'/tmp/{prj_name}.log'


    #- override configuration logger with input parameters
    if inp_log.console: log['console']=inp_log.console
    if inp_log.modules: log['modules']=inp_log.modules
    if inp_log.level: log['level']=inp_log.level


    lnLogger = setLogger(log)
    _myGlobalInitialSettings['logger']=lnLogger # update

    lnLogger.debug3('input   arguments', args.__dict__)
    lnLogger.debug3('logging arguments', inp_log)
    lnLogger.debug3('debug   arguments', dbg.__dict__)
    lnLogger.debug3('configuration data', dConfig)
    # -------------------------------
    gv.logger=lnLogger
    gv.TAB='   [Ln]: '


    # ---- inizializzazione di alcuni moduli che utilizzano i global values...
    prompt(gVars=_myGlobalInitialSettings)
    MountUmount.setup(gVars=_myGlobalInitialSettings)
    DeviceList.setup(gVars=_myGlobalInitialSettings)
    DisplayDevice.setup(gVars=_myGlobalInitialSettings)
    # ----


    # ---- legge i device disponibili (lsblk)
    req_mpoint=args.mpoint if 'mpoint' in args else None
    device_list=DeviceList.deviceList(dConfig['UUIDs'], req_mpoint=req_mpoint)

    if args.action=='list':
        for name, _device in device_list.items():
            display(_device)
        print()
        sys.exit()

    rCode=1
    for name, my_dev in device_list.items():
        _device=SimpleNamespace(**my_dev)
        if name==args.device_name or _device.uuid==args.uuid or _device.partuuid==args.partuuid:
            C.pYellow('''
                -----------------------------------
                - required device - current status
                ----------------------------------- ''', tab=4)
            display(my_dev)
            if args.action=='mount':
                rCode=MountUmount.mount(my_dev, fEXECUTE=dbg.go)
                break
            elif args.action=='umount':
                rCode=MountUmount.umount(my_dev, fEXECUTE=dbg.go)
                break

    #- display current status
    if rCode==0:
        device_list=DeviceList.deviceList(dConfig['UUIDs'], req_mpoint)
        my_dev=device_list[_device.name]
        C.pYellow('''

            ----------------------------------------------
            - required device - status after operation
            ---------------------------------------------- ''', tab=4)
        display(my_dev)

    msg = "     program completed."
    print ()
    print (msg)
    print ()
