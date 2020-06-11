#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 11-06-2020 15.09.39
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
import pdb



# def DeviceStatus(gv, device_list, req_name=None, req_partuuid=None, req_uuid=None):
def DeviceStatus(gv, device_list):
    global C, mpForced
    logger=gv.lnLogger
    C=gv.Color
    inpArgs=gv.inpArgs

    mpForced=False


    # vediamo se il device richiesto esiste
    req_device_name=None
    for name, data in device_list.items():
        if name==inpArgs.device_name or data.uuid==inpArgs.uuid or data.partuuid==inpArgs.partuuid:
            req_device_name=name
            break

    if req_device_name:
        if gv.pdb: pdb.set_trace()
        dev=device_list[req_device_name]
        if not dev.mountpoint:
            if inpArgs.mpoint:
                dev.mountpoint=inpArgs.mpoint
            else:
                dev.mountpoint='/mnt/{data.label}-{data.partuuid}'.format(**locals())
                mpForced=True

        display(device_list, req_device_name)
        dev=dev.toDict()

    else:
        display(device_list)
        print()
        C.magentaH(text='''
            Immettere uno dei device in lista''', tab=4)
        print()
        dev={}


    return dev




def display(devices, req_device_name=None):
    for name, data in devices.items():
        if req_device_name and not name==req_device_name: continue
        C.yellowH(text=name, tab=4)

        C.cyan(text='{:12}: {}'.format('name', data.name), tab=8)
        C.cyan(text='{:12}: {}'.format('label', data.label), tab=8)
        C.cyan(text='{:12}: {}'.format('path', data.path), tab=8)
        C.cyanH(text='{:12}: {}'.format('uuid', data.uuid), tab=8)
        C.cyan(text='{:12}: {}'.format('partuuid', data.partuuid), tab=8)
        C.cyan(text='{:12}: {}'.format('size', data.size), tab=8)
        C.cyan(text='{:12}: {}'.format('fstype', data.fstype), tab=8)

        if mpForced and (not data.mounted):
            msg="  ---> dynamically calculated. Use --mpoint arg to specify your own."
            mp=data.mountpoint + C.yellowH(text=msg, get=True)
        else:
            mp=data.mountpoint
        C.cyanH(text='{:12}: {}'.format('mountpoint', mp), tab=8)

        C.whiteH(text='{:12}: {}'.format('------', '------'), tab=8)

        color=C.greenH if data.mounted else C.magentaH
        color(text='{:12}: {}'.format('mounted', data.mounted), tab=8)

        print()