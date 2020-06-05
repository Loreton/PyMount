#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 05-06-2020 10.41.42
#
# -----------------------------------------------

import sys
import argparse

##############################################################
# - Parse Input
##############################################################
def parseInput():
    # =============================================
    # = Parsing
    # =============================================
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='Main parser')

    subparsers = parser.add_subparsers(title="actions")

    # -----------------------
    # - mount parser
    # -----------------------
    mount_parser  = subparsers.add_parser ("mount", help = "mount device")


    # -----------------------
    # - umount parser
    # -----------------------
    umount_parser = subparsers.add_parser ("umount", help="umount a device")

    # -----------------------
    # - list parser
    # -----------------------
    list_parser = subparsers.add_parser ("list", help="list devices")


    args = parser.parse_args()
    # print (args); sys.exit()

    # - creiamo una entri 'action' con il nome del subparser scelto
    for name, subp in subparsers.choices.items():
        if name in args:
            args.action = name

    # if args.log_console or args.log_modules:
    #     args.log=True

    # if args.display_args:
    #     import json
    #     json_data = json.dumps(vars(args), indent=4, sort_keys=True)
    #     print('input arguments: {json_data}'.format(**locals()))
    #     sys.exit(0)


    return  args

