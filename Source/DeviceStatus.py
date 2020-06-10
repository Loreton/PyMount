#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 10-06-2020 09.49.47
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
import pdb



# ###########################################################################
# #
# ###########################################################################
def checkPartUUID(device_list, req_partuuid):
    dev={}
    for name, data in device_list.items():
        if data.partuuid==req_partuuid:
            dev[name]=device_list.pop(name)
            break
    return dev


# ###########################################################################
# #
# ###########################################################################
def checkUUID(device_list, req_uuid):

    dev={}
    for name, data in device_list.items():
        if data.uuid==req_uuid:
            dev[name]=device_list.pop(name)
            break
    return dev

# ###########################################################################
# #
# ###########################################################################
def checkName(device_list, req_name):

    dev={}
    for name, data in device_list.items():
        if data.name==req_name:
            dev[name]=device_list.pop(name)
            break
    return dev






def DeviceStatus(gv, device_list, req_name=None, req_partuuid=None, req_uuid=None):
    logger=gv.lnLogger
    C=gv.Color


    if gv.pdb_trace: pdb.set_trace()
    dev3=checkName(device_list, req_name)
    dev1=checkPartUUID(device_list, req_partuuid)
    dev2=checkUUID(device_list, req_uuid)
    dev={}
    if   dev1:
        dev=dev1
    elif dev2:
        dev=dev2
    elif dev3:
        dev=dev3

    if not dev:
        print()
        C.magentaH(text='''
            Il device richiesto non è stato trovato.
            Immettere uno dei seguenti:''', tab=4)
        print()
    else:
        device_list=dev


    for device, data in device_list.items():
        C.yellowH(text=device, tab=4)

        C.cyanH(text='{:12}: {}'.format('name', data.name), tab=8)
        C.cyanH(text='{:12}: {}'.format('label', data.label), tab=8)
        C.cyanH(text='{:12}: {}'.format('path', data.path), tab=8)
        C.cyanH(text='{:12}: {}'.format('uuid', data.uuid), tab=8)
        C.cyanH(text='{:12}: {}'.format('partuuid', data.partuuid), tab=8)
        C.cyanH(text='{:12}: {}'.format('size', data.size), tab=8)
        C.cyanH(text='{:12}: {}'.format('fstype', data.fstype), tab=8)
        C.magentaH(text='{:12}: {}'.format('mountpoint', data.mountpoint), tab=8)

        print()

    return dev

