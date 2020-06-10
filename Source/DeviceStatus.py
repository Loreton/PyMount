#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 10-06-2020 16.51.37
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
import pdb



def DeviceStatus(gv, device_list, req_name=None, req_partuuid=None, req_uuid=None):
    global C
    logger=gv.lnLogger
    C=gv.Color
    config=gv.config


    if gv.pdb_trace: pdb.set_trace()
    req_device_name=None
    for name, data in device_list.items():
        if name==req_name or data.uuid==req_uuid or data.partuuid==req_partuuid:
            req_device_name=name
            break

    fERROR=False
    if req_device_name:
        dev=device_list[req_device_name]
        # if not dev.mountpoint:
        #     msg="---> mountpoint not specified. Please modify configuration file."
        #     dev.mountpoint='None ' + C.redH(text=msg, get=True)
        #     fERROR=True

        display(device_list, req_device_name)
        if fERROR:
            sys.exit(1)
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

        if not data.mountpoint:
            msg="---> if not specified will be mounted on /mnt/{data.label}-{data.uuid}".format(**locals())
            mp='None ' + C.yellowH(text=msg, get=True)
        else:
            mp=data.mountpoint
        C.cyanH(text='{:12}: {}'.format('mountpoint', mp), tab=8)

        C.whiteH(text='{:12}: {}'.format('------', '------'), tab=8)

        color=C.greenH if data.mounted else C.magentaH
        color(text='{:12}: {}'.format('mounted', data.mounted), tab=8)

        print()