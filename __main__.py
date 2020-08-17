#!/usr/local/bin/python3
# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 17-08-2020 17.42.38
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

# - può essere inviato solo al primo richiamodella funzione/modulo
_myGlobalInitialSettings={'logger': nullLogger(), 'color': LnColor()}

import types # for SimpleNamespace()

from LnLib.yamlLoaderLN import loadYamlFile
from LnLib.loggerLN     import setLogger
from LnLib.promptLN     import prompt
from LnLib              import pathMonkeyFunctionsLN # necessario per i miei comandi di Path (tra cui file.sizeRotate())


from Source.parseInputLN import parseInput
# from Source.DeviceStatus import deviceStatus
from Source.DeviceList   import deviceList
# from Source.MountUmount  import mount, umount
from Source import MountUmount
from Source.DisplayDevice  import display

######################################
# sample call:
#
######################################
if __name__ == '__main__':
    gv=types.SimpleNamespace()

    prj_dir=Path(sys.argv[0]).resolve().parent

    # Questo step serve per quando siamo all'interno dello zip
    if prj_dir.stem=='bin': prj_dir=prj_dir.parent
    prj_name=prj_dir.stem
    prj_name='pymount'

    os.environ['Prj_Name']=prj_name.lower() # potrebbe usarla loadYamlFile()

    ''' read Main configuration file '''
    dConfig=loadYamlFile(f'conf/{prj_name.lower()}.yml', resolve=True, fPRINT=False)

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
    _myGlobalInitialSettings['logger']=lnLogger
    prompt(gVars=_myGlobalInitialSettings)
    MountUmount.setup(gVars=_myGlobalInitialSettings)
    # ----


    # ---- legge i device disponibili (lsblk)
    device_list=deviceList(dConfig['UUIDs'], gVars=_myGlobalInitialSettings)
    if args.action=='list':
        for name, _device in device_list.items():
            display(_device)
        print()
        sys.exit()

    for name, my_dev in device_list.items():
        _device=SimpleNamespace(**my_dev)
        if name==args.device_name or _device.uuid==args.uuid or _device.partuuid==args.partuuid:
            display(my_dev)
            if args.action=='mount':
                MountUmount.mount(my_dev, fEXECUTE=dbg.go)
                break
            elif args.action=='umount':
                MountUmount.umount(my_dev, fEXECUTE=dbg.go)
                break


    msg = "     program completed."
    print ()
    print (msg)
    print ()
