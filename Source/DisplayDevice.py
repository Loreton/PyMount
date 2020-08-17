#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 17-08-2020 17.08.03
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
from LnLib.colorLN import LnColor; C=LnColor()
from types import SimpleNamespace


#############################################################
# if sigle_device: just a single device will be displayed.
#############################################################
def display(device):
    _device=SimpleNamespace(**device)
    C.pYellowH(_device.name, tab=4)

    C.pCyan( f'name:        {_device.name}', tab=8)
    C.pCyan( f'label:       {_device.label}', tab=8)
    C.pCyan( f'path:        {_device.path}', tab=8)
    C.pCyanH(f'uuid:        {_device.uuid}', tab=8)
    C.pCyan( f'partuuid:    {_device.partuuid}', tab=8)
    C.pCyan( f'size:        {_device.size}', tab=8)
    C.pCyan( f'fstype:      {_device.fstype}', tab=8)

    mp=_device.mountpoint

    if not _device.mounted and _device.mp_dynamic:
        color=C.pYellowH
        status=''' NOT mounted  ---> mp is dynamically calculated.
                    Use --mpoint arg or change config file to specify your own.
                    '''
    elif _device.mounted:
        color=C.pGreenH
        status='already mounted'
    else:
        color=C.pMagentaH
        status='NOT mounted'

    color(f'mountpoint:  {mp}   - {status}', tab=8)

    print()