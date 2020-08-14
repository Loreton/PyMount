#!/usr/bin/python3.5
#
# updated by ...: Loreto Notarantonio
# Version ......: 11-06-2020 15.08.39
#
# -----------------------------------------------

import sys
import argparse


def common_options(my_parser):

    # -- add common options to my_parser
    help_color='white'


    # --- common
    my_parser.add_argument('--go', action='store_true', help=c_green('load data. default is --dry-run'))

    my_parser.add_argument('--display-args', action='store_true', help=c_green('Display input paramenters'))
    my_parser.add_argument('--pdb', action='store_true', help=c_green('attiva il debug del pdb'))
    my_parser.add_argument('--debug', action='store_true', help=c_green('display paths and input args'))
    my_parser.add_argument('--log', action='store_true', help=c_green('activate log.'))
    my_parser.add_argument('--log-console', action='store_true', help=c_green('activate log and write to console too.'))
    my_parser.add_argument('--log-modules',
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
    # if len(sys.argv) == 1:
    #     sys.argv.append('list')

    parser = argparse.ArgumentParser(description='Main parser')

    mount_group = parser.add_mutually_exclusive_group(required=False)
    mount_group.add_argument('--uuid', help='specify disk UUID', default=None)
    mount_group.add_argument('--partuuid', help='specify disk PARTUUID', default=None)
    mount_group.add_argument('--device-name', help='specify device name', default=None)
    parser.add_argument('--mpoint', help='specify device mountpoint direcotry (DEFAULT: LABEL-PARTUUID)', default=None)

    # - common options
    common_options(parser)


    args = parser.parse_args()
    # print (args); sys.exit()


    if args.log_console or args.log_modules:
        args.log=True

    if args.display_args:
        import json
        json_data = json.dumps(vars(args), indent=4, sort_keys=True)
        print('input arguments: {json_data}'.format(**locals()))
        sys.exit(0)


    return  args

