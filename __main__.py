#!/usr/local/bin/python3
# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 05-06-2020 13.40.08
#
# #############################################

import sys; sys.dont_write_bytecode = True
import os
from   pathlib import Path
from dotmap import DotMap
import pdb

# import Source as Prj

from Source.ReadConfigurationFile import readConfigFile
from Source.ParseInput import parseInput
# import LnLib as Ln
# Ln=Prj.LnLib          # --- se faccio import all'interno di Source/__init__.py


######################################
# sample call:
#
######################################
if __name__ == '__main__':

    # -------------------------------
    # - parse input parameters
    # -------------------------------
    inpArgs=parseInput()
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
    lnLogger = Ln.setLogger(filename=log_file, console=fCONSOLE, debug_level=3, log_modules=inpArgs.log_modules, color=Ln.Color() )

    lnLogger.info('input arguments', vars(inpArgs))
    lnLogger.info('configuration data', _data)
    Path.LnSet(lnLogger)

    C    = Ln.Color()
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



    if 'mount' in inpArgs.action:
        mount(gv)

    elif 'umount' in inpArgs.action:
        umount(gv)

    else:
        list(gv)

    msg = "     program completed."
    print ()
    print (msg)
    print ()
    # Ln.Exit(0, msg)
