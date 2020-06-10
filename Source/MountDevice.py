#!/usr/bin/python3
#
# updated by ...: Loreto Notarantonio
# Version ......: 10-06-2020 09.50.20
#
# -----------------------------------------------
import sys; sys.dont_write_bytecode = True
import subprocess

# ###########################################################################
# #
# ###########################################################################
def MountDevice(gv, req_device):
    logger=gv.lnLogger
    C=gv.Color

    print(req_device)