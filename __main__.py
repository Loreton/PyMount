#!/usr/local/bin/python3
# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 24-09-2020 14.50.58
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


import types # for SimpleNamespace()

from LnLib.yamlLoaderLN import loadYamlFile
from LnLib.loggerLN     import setLogger
from LnLib.promptLN     import prompt
from LnLib              import monkeyPathLN # necessario per i miei comandi di Path (tra cui file.sizeRotate())


from Source.parseInputLN import parseInput
from Source import DeviceList
from Source import MountUmount
from Source import DisplayDevice; display=DisplayDevice.display


def get_my_dev(config, args, all_devices=False, fPRINT=False):
    req_mpoint=args.mpoint if 'mpoint' in args else None
    device_list=DeviceList.deviceList(config, req_mpoint=req_mpoint)

    if all_devices:
        lnLogger.debug('DEVICES found:', device_list)
        if fPRINT:
            for name, _device in device_list.items():
                display(_device, msg='current status')
            print()
        return device_list

    lnLogger.info('DEVICE required:', args)
    for name, my_dev in device_list.items():

        _device=SimpleNamespace(**my_dev)

        args_name=getattr(args, 'name', None)
        args_uuid=getattr(args, 'uuid', None)
        args_partuuid=getattr(args, 'partuuid', None)

        if name==args_name or _device.uuid==args_uuid or _device.partuuid==args_partuuid:
            lnLogger.info('DEVICE found:', my_dev)
            return my_dev

    lnLogger.info('NO DEVICE found:')
    return None



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

    lnLogger.debug3('input   arguments', args.__dict__)
    lnLogger.debug3('logging arguments', inp_log)
    lnLogger.debug3('debug   arguments', dbg.__dict__)
    lnLogger.debug3('configuration data', dConfig)
    # -------------------------------
    gv.logger=lnLogger
    gv.TAB='   [Ln]: '


    # ---- inizializzazione di alcuni moduli che utilizzano i global values...
    _myGlobal={'logger': lnLogger, 'color': LnColor()}
    prompt(gVars=_myGlobal)
    MountUmount.setup(gVars=_myGlobal)
    DisplayDevice.setup(gVars=_myGlobal)
    # ----
    if args.action=='list':
        device_list=get_my_dev(dConfig['UUIDs'], args, all_devices=True, fPRINT=True)
        sys.exit()

    # ---- legge i device disponibili (lsblk)
    my_dev=get_my_dev(dConfig['UUIDs'], args)
    if not my_dev:
        C.pError(text='Required device was NOT found', tab=4)
        sys.exit()


    if args.action=='mount':
        display(my_dev, msg=f'status before {args.action}')
        rCode=MountUmount.mount(my_dev, fEXECUTE=dbg.go)

    elif args.action=='umount':
        display(my_dev, msg=f'status before {args.action}')
        rCode=MountUmount.umount(my_dev, fEXECUTE=dbg.go)

    elif args.action=='remount':
        display(my_dev, msg=f'status before {args.action}')
        rCode=MountUmount.umount(my_dev, fEXECUTE=dbg.go)
        if rCode==0:
            my_dev=get_my_dev(dConfig['UUIDs'], args) # re-read device status
            rCode=MountUmount.mount(my_dev, fEXECUTE=dbg.go)





    # display(my_dev, msg=f'status after {args.action}')
    #- display current status
    # print(rCode)
    if rCode==0:
        my_dev=get_my_dev(dConfig['UUIDs'], args)
        display(my_dev, msg=f'status after {args.action}')

    msg = "     program completed."
    print ()
    print (msg)
    print ()
