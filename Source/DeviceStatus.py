#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 16-08-2020 12.45.32
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
from LnLib.colorLN import LnColor; C=LnColor()
from LnLib.nameSpaceLN import RecursiveNamespace
from types import SimpleNamespace




##########################################################
#
##########################################################
def deviceStatus(inpArgs, devices, gVars={}):
    if gVars:
        global C
        if 'color' in gVars: C=gVars['color']

    global mpForced
    mpForced=False
    # devices=RecursiveNamespace(**devices)

    # vediamo se il device richiesto esiste

    my_dev={}
    for name, data in devices.items():
        _device=SimpleNamespace(**data)
        if name==inpArgs.device_name or _device.uuid==inpArgs.uuid or _device.partuuid==inpArgs.partuuid:
            my_dev=data
            break




    # import pdb; pdb.set_trace() # by Loreto
    if my_dev:
        _device=SimpleNamespace(**my_dev)
        if not _device.mountpoint: # if not already defined
            if inpArgs.mpoint:  # ... get from input
                _device.mountpoint=inpArgs.mpoint
            else: # .. or force a default mountpoint
                _device.mountpoint=f'/mnt/{_device.label}-{_device.partuuid}'
                mpForced=True

        display(my_dev)
        # my_dev=my_dev.toDict()

    else:
        for name, _device in devices.items():
            display(_device)
        print()
        C.pMagentaH(text='''
            Immettere uno dei device in lista''', tab=4)
        print()


    return my_dev # dictionary



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

    if mpForced and (not _device.mounted):
        msg="  ---> dynamically calculated. Use --mpoint arg to specify your own."
        mp=_device.mountpoint + C.YellowH(text=msg)
    else:
        mp=_device.mountpoint

    if _device.mounted:
        color=C.pGreenH
        status='already mounted'
    else:
        color=C.pMagentaH
        status='NOT mounted'
    color(f'mountpoint:  {mp}   - {status}', tab=8)

    print()