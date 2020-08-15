#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 15-08-2020 18.59.32
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
from LnLib.colorLN import LnColor; C=LnColor()
from LnLib.nameSpaceLN import RecursiveNamespace


def _set(Color)
    gobal C
    C=Color()


##########################################################
#
##########################################################
def DeviceStatus(inpArgs, devices):
    global mpForced
    mpForced=False
    devices=RecursiveNamespace(**devices)

    # vediamo se il device richiesto esiste
    req_device_name=None

    for name, data in devices.__dict__.items():
        if name==inpArgs.device_name or data.uuid==inpArgs.uuid or data.partuuid==inpArgs.partuuid:
            req_device_name=name
            break

    if req_device_name:
        if gv.pdb: pdb.set_trace()
        dev=devices[req_device_name]
        if not dev.mountpoint:
            if inpArgs.mpoint:
                dev.mountpoint=inpArgs.mpoint
            else:
                dev.mountpoint=f'/mnt/{data.label}-{data.partuuid}'
                mpForced=True

        display(devices, req_device_name)
        dev=dev.toDict()

    else:
        display(devices)
        print()
        C.pMagentaH(text='''
            Immettere uno dei device in lista''', tab=4)
        print()
        dev={}


    return dev




def display(devices, req_device_name=None):
    for name, data in devices.__dict__.items():
        if req_device_name and not name==req_device_name: continue

        C.pYellowH(name, tab=4)

        C.pCyan( f'name:        {data.name}', tab=8)
        C.pCyan( f'label:       {data.label}', tab=8)
        C.pCyan( f'path:        {data.path}', tab=8)
        C.pCyanH(f'uuid:        {data.uuid}', tab=8)
        C.pCyan( f'partuuid:    {data.partuuid}', tab=8)
        C.pCyan( f'size:        {data.size}', tab=8)
        C.pCyan( f'fstype:      {data.fstype}', tab=8)

        if mpForced and (not data.mounted):
            msg="  ---> dynamically calculated. Use --mpoint arg to specify your own."
            mp=data.mountpoint + C.YellowH(text=msg)
        else:
            mp=data.mountpoint
        C.pCyanH(f'mountpoint:  {mp}', tab=8)

        C.pWhiteH('------:      ------', tab=8)

        color=C.pGreenH if data.mounted else C.pMagentaH
        color(f'mounted: {data.mounted}', tab=8)

        print()