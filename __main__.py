#!/usr/local/bin/python3
# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 09-06-2020 18.26.10
#
# #############################################

import sys; sys.dont_write_bytecode = True
import os
from   pathlib import Path
from dotmap import DotMap
import pdb
import subprocess

# import Source as Prj

from Source.ReadConfigurationFile import readConfigFile
from Source.ParseInput import parseInput
import LnLib as Ln
# Ln=Prj.LnLib          # --- se faccio import all'interno di Source/__init__.py

from Source.DeviceList import DeviceList as deviceList

######################################
# sample call:
#
######################################
if __name__ == '__main__':

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
        log_file = os.path.abspath(os.path.join(log_dir, '{prj_name}_{inpArgs.action}.log'.format(**locals())))
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
    gv.inpArgs  = inpArgs
    gv.config   = config
    # -----------------------------------------------

    device_list=deviceList(gv)
    req_device={}
    for device, data in device_list.items():
        if (inpArgs.device_name) and (device==inpArgs.device_name):
            req_device[device]=device_list.pop(device)
        elif (inpArgs.partuuid) and ('partuuid' in data) and (data.partuuid==inpArgs.partuuid):
            req_device[device]=device_list.pop(device)
        elif (inpArgs.uuid) and ('uuid' in data) and (data.uuid==inpArgs.uuid):
            req_device[device]=device_list.pop(device)

        if req_device:
            device_list=req_device

    mounted = subprocess.check_output('/bin/mount', stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
    mounted = mounted.decode('utf-8').split('\n')       # converti in STRing/LIST


    for device, data in device_list.items():
        C.yellowH(text=device, tab=4)
        if 'label' in data:     C.cyanH(text='{:12}:{}'.format('LABEL', data.label), tab=8)
        if 'uuid' in data:      C.cyanH(text='{:12}:{}'.format('UUID', data.uuid), tab=8)
        if 'partuuid' in data:  C.cyanH(text='{:12}:{}'.format('PARTUUID', data.partuuid), tab=8)
        if 'size' in data:      C.cyanH(text='{:12}:{}'.format('SIZE', data.size), tab=8)
        if 'fstype' in data:    C.cyanH(text='{:12}:{}'.format('FSTYPE', data.fstype), tab=8)
        for item in mounted:
            if not item.strip(): continue
            token=item.split()
            if device == token[0]:
                C.magentaH(text='{:10}:{}'.format('mounted on', token[2]), tab=8)
        print()






    # if 'mount' in inpArgs.action:
    #     mount(gv)

    # elif 'umount' in inpArgs.action:
    #     umount(gv)

    # else:
    #     list(gv)

    msg = "     program completed."
    print ()
    print (msg)
    print ()
    # Ln.Exit(0, msg)
