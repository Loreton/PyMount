#!/usr/local/bin/python3
# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 14-08-2020 16.55.58
#
# #############################################

import sys; sys.dont_write_bytecode = True
import os
from   pathlib import Path
from dotmap import DotMap
import pdb
# import subprocess


import types # for SimpleNamespace()

from LnLib.yamlLoaderLN import loadYamlFile
from LnLib.loggerLN import setLogger
# from LnLib.sshClassLN import LnSSH
from LnLib import pathMonkeyFunctionsLN # server per i miei comandi di Path (tra cui file.sizeRotate())


from Source.parseInputLN import parseInput

# import Source as Prj
# from LnLib.yamlLoader import loadYamlFile
# from LnLib.LnLogger import setLogger
# from LnLib.LnColor import LnColor; C=LnColor()

# from Source.Main.ParseInput import parseInput
# from Source.Functions.Crontab import Crontab
# from LnLib.yamlLoaderLN import loadYamlFile
# from LnLib.loggerLN import setLogger
# from LnLib.sshClassLN import LnSSH
# from LnLib import pathMonkeyFunctionsLN # server per i miei comandi di Path (tra cui file.sizeRotate())

# from Source.ParseInput import parseInput

# from Source.ReadConfigurationFile import readConfigFile
# from Source.ParseInput import parseInput

from Source.DeviceList import DeviceList as deviceList
from Source.DeviceStatus import DeviceStatus as deviceStatus
from Source.MountDevice import MountDevice as mountDevice

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

    os.environ['Prj_Name']=prj_name # potrebbe usarla loadYamlFile()

    ''' read Main configuration file '''
    dConfig=loadYamlFile(f'conf/{prj_name}.yml', resolve=True, fPRINT=False)

    ''' parsing input '''
    args, inp_log, dbg=parseInput(server_list=dConfig['servers'], module_list=list(dConfig['modules']))

    ''' logger '''
    log=dConfig['logger']
    log['filename']=f'/tmp/{prj_name}.log'


    #- override configuration logger with input parameters
    if inp_log.console: log['console']=inp_log.console
    if inp_log.modules: log['modules']=inp_log.modules
    if inp_log.level: log['level']=inp_log.level


    lnLogger = setLogger(log)
    lnLogger.debug3('input   arguments', vars(args))
    lnLogger.debug3('logging arguments', inp_log)
    lnLogger.debug3('debug   arguments', vars(dbg))
    lnLogger.debug3('configuration data', dConfig)
    # -------------------------------
    gv.logger=lnLogger
    gv.TAB='   [Ln]: '





if __name__ == 'xxx__main__':

    # -------------------------------
    # - parse input parameters
    # -------------------------------
    inpArgs=parseInput(Ln.Color())
    # fCONSOLE=inpArgs.log_console

    # -------------------------------
    # - read configuration file
    # -------------------------------
    _data            = readConfigFile(filename='LnMount', fPRINT=False)
    config           = DotMap(_data['content'])
    prj_name         = _data['prjname']
    script_path      = _data['script_path']
    yaml_config_file = _data['yaml_config_file']

    # -------------------------------
    # - Inizializzazione del logger
    # -------------------------------
    if inpArgs.log:
        log_dir  = os.path.join(script_path, 'log')
        log_file = os.path.abspath(os.path.join(log_dir, '{prj_name}.log'.format(**locals())))
    else:
        log_file = None
    lnLogger = Ln.setLogger(filename=log_file, console=inpArgs.log_console, debug_level=3, log_modules=inpArgs.log_modules, color=Ln.Color() )

    lnLogger.info('input arguments', vars(inpArgs))
    lnLogger.info('configuration data', _data)
    Path.LnSet(lnLogger)

    C = Ln.Color()
    if inpArgs.debug:
        C.setColor(color=C._cyanH)
        print('     Input arguments:')
        for k,v in vars(inpArgs).items():
            print('         {k:<15}: {v}'.format(**locals()))
        print()
        C.setColor(color=C._yellowH)
        print('     {0:<15}: {1}'.format('prj_name', prj_name))
        print('     {0:<15}: {1}'.format('ScriptDir', str(script_path)))
        print('     {0:<15}: {1}'.format('config file', yaml_config_file))
        print()
        sys.exit(1)

    # -------------------------------
    # - set global variables
    # -------------------------------
    gv          = DotMap(_dynamic=False)
    gv.Ln       = Ln
    gv.lnLogger = lnLogger
    gv.Color    = C
    gv.pdb      = inpArgs.pdb
    gv.inpArgs  = inpArgs
    gv.config   = config
    # -----------------------------------------------

    # legge i device disponibili (lsblk)
    device_list=deviceList(gv)

    # prende tutti i paramentri
    # mount_device=deviceStatus(gv, device_list=device_list, req_name=inpArgs.device_name, req_partuuid=inpArgs.partuuid, req_uuid=inpArgs.uuid)
    mount_device=deviceStatus(gv, device_list=device_list)

    # pdb.set_trace()
    if mount_device:
        mountDevice(gv, mount_device, fEXECUTE=inpArgs.go)


    msg = "     program completed."
    print ()
    print (msg)
    print ()
    # Ln.Exit(0, msg)
