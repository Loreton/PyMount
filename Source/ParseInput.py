#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 05-06-2020 17.16.41
#
# -----------------------------------------------

import sys
import argparse


def common_options(subparsers):

    # -- add common options to all subparsers
    for name, subp in subparsers.choices.items():
        # print(name)
        # print(subp)
        help_color='white'
        # --- mi serve per avere la entry negli args e creare poi la entry "action"
        subp.add_argument('--{0}'.format(name), action='store_true', default=True)

        # --- common
        subp.add_argument('--go', action='store_true', help=c_green('load data. default is --dry-run'))

        subp.add_argument('--display-args', action='store_true', help=c_green('Display input paramenters'))
        subp.add_argument('--debug', action='store_true', help=c_green('display paths and input args'))
        subp.add_argument('--log', action='store_true', help=c_green('activate log.'))
        subp.add_argument('--log-console', action='store_true', help=c_green('activate log and write to console too.'))
        subp.add_argument('--log-modules',
                                    metavar='',
                                    required=False,
                                    default=[],
                                    nargs='*',
                                    help=c_green("""activate log.
        E' anche possibile indicare una o più stringhe separate da BLANK
        per identificare le funzioni che si vogliono filtrare nel log.
        Possono essere anche porzioni di funcName. Es: --log-module nudule1 module2 module3
        """))


def c_yellow(text):
    if Color:
        text=Color.yellow(text=text, get=True)
    return text

def c_green(text):
    if Color:
        text=Color.green(text=text, get=True)
    return text



##############################################################
# - Parse Input
##############################################################
def parseInput(color=None):
    global Color
    Color=color
    # =============================================
    # = Parsing
    # =============================================
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser(description='Main parser')
    subparsers = parser.add_subparsers(title="actions")


    # - mount parser
    mount_parser  = subparsers.add_parser ("mount", help = "mount device")


    # - umount parser
    umount_parser = subparsers.add_parser ("umount", help="umount a device")

    # - list parser
    list_parser = subparsers.add_parser ("list", help="list devices")


    # - common options
    common_options(subparsers)


    args = parser.parse_args()
    # print (args); sys.exit()

    # - creiamo una entry 'action' che conterrà il nome del subparser scelto
    for name, subp in subparsers.choices.items():
        if name in args:
            args.action = name

    if args.log_console or args.log_modules:
        args.log=True

    if args.display_args:
        import json
        json_data = json.dumps(vars(args), indent=4, sort_keys=True)
        print('input arguments: {json_data}'.format(**locals()))
        sys.exit(0)


    return  args

