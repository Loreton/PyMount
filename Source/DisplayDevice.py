#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 24-09-2020 14.38.29
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
from colorLN import LnColor; C=LnColor()
from types import SimpleNamespace



# ###########################################################################
# # set logger and color
# ###########################################################################
# def setup(gVars):
#     global C, logger
#     if 'color' in gVars: C=gVars['color']
#     if 'logger' in gVars: logger=gVars['logger']

#############################################################
# if sigle_device: just a single device will be displayed.
#############################################################
def display(device, msg):
    _device=SimpleNamespace(**device)
    C.pYellow(f'''
        ----------------------------------------------
        - [{_device.path}] {msg}
        ---------------------------------------------- ''', tab=4)
    C.pYellowH(_device.name, tab=4)

    C.pCyan( f'name:        {_device.name}', tab=8)
    C.pCyan( f'label:       {_device.label}', tab=8)
    C.pCyan( f'path:        {_device.path}', tab=8)
    C.pCyanH(f'uuid:        {_device.uuid}', tab=8)
    C.pCyan( f'partuuid:    {_device.partuuid}', tab=8)
    C.pCyan( f'size:        {_device.size}', tab=8)
    C.pCyan( f'fstype:      {_device.fstype}', tab=8)

    mp=_device.mountpoint

    if not _device.mounted and _device.dynamic_mp:
        color=C.pYellowH
        status=''' NOT mounted  ---> mp is dynamically calculated.
                    Use --mpoint arg or change config file to specify your own.
                    '''
    elif _device.mounted:
        color=C.pGreenH
        status='mounted'
    else:
        color=C.pMagentaH
        status='NOT mounted'

    color(f'mountpoint:  {mp}   - {status}', tab=8)

    print()