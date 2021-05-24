# #############################################
#
# updated by ...: Loreto Notarantonio
# Version ......: 24-09-2020 08.27.54
#
# #############################################

import sys
import argparse
from pathlib import Path
from colorLN import LnColor; C=LnColor()

# def common_options(my_parser):
#     my_parser.add_argument('------------  debug options', action='store_true')
#     my_parser.add_argument('--go', action='store_true', help='default is --dry-run')
#     my_parser.add_argument('--display-args', action='store_true', help='Display input paramenters')
#     my_parser.add_argument('--debug', action='store_true',
#                                 help='''display paths and input args\n\n'''+C.gGreen())


#     my_parser.add_argument('------------  overriding log options', action='store_true')
#     my_parser.add_argument('--log-level', type=str, default='info',
#                             choices=['critical','error','warning','info','debug1','debug2','debug3'],
#                             help='specify log level.')
#     my_parser.add_argument('--log-console', action='store_true',
#                             help='Activate log and write to console too.')

#     my_parser.add_argument('--log-modules',
#                                 metavar='',
#                                 required=False,
#                                 default=[],
#                                 nargs='*',
#                                 help="""Activate log.
#     E' anche possibile indicare una o più stringhe separate da BLANK
#     per identificare le funzioni che si vogliono filtrare nel log.
#     Possono essere anche porzioni di funcName.
#     Es: --log-module nudule1 module2 module3
#         """)


def common_options(my_parser):

    my_parser.add_argument('------------  debug options', action='store_true')
    my_parser.add_argument('--display-args', action='store_true', help='Display input paramenters')
    my_parser.add_argument('--debug', action='store_true',
                                help='''display paths and input args\n\n'''+C.gGreen())
                                # help='''display paths and input args\n\n''')

    my_parser.add_argument('------------  overriding log options', action='store_true')
    # my_parser.add_argument('--log-console', action='store_true',
    #                         help='Activate log and write to console too.')

    my_parser.add_argument( "--log-console",
                            metavar='<log--console-level>',
                            type=str,
                            default='critical',
                            choices=['critical','error','warning','info','debug'],
                            help='specify console log level and activate it.'
                        )




    my_parser.add_argument('--log-exclude',
                                metavar='',
                                required=False,
                                default=[],
                                nargs='*',
                                help="""Activate log.
    E' anche possibile indicare una o più stringhe separate da BLANK
    per identificare le funzioni che si vogliono filtrare nel log.
    Possono essere anche porzioni di funcName.
    Es: --log-module nudule1 module2 module3
        """)

    my_parser.add_argument('--log-include',
                                metavar='',
                                required=False,
                                default=[],
                                nargs='*',
                                help="""Activate log.
    E' anche possibile indicare una o più stringhe separate da BLANK
    per identificare le funzioni che si vogliono filtrare nel log.
    Possono essere anche porzioni di funcName.
    Es: --log-module nudule1 module2 module3
        """)





##############################################################
# - MAin Options
##############################################################
def mainOptions(parser):
    subparsers=parser.add_subparsers(title="primary commands",
                                    dest='action',
                                    help='commands'+C.gYellow())

    # - mount parser
    mount_parser=subparsers.add_parser("mount",
                        formatter_class=argparse.RawTextHelpFormatter,
                        help="mount process")
    mount_parser.add_argument('--mpoint', help='specify mount point', default=None)
    mount_group=mount_parser.add_mutually_exclusive_group(required=True)
    mount_group.add_argument('--uuid', help='specify disk UUID', default=None)
    mount_group.add_argument('--partuuid', help='specify disk PARTUUID', default=None)
    mount_group.add_argument('--device-name', help='specify device name\n\n'+C.gBlue(),default=None)

    # - umount parser
    umount_parser=subparsers.add_parser("umount",
                        formatter_class=argparse.RawTextHelpFormatter,
                        help="umount process")
    umount_group=umount_parser.add_mutually_exclusive_group(required=True)
    umount_group.add_argument('--uuid', help='specify disk UUID', default=None)
    umount_group.add_argument('--partuuid', help='specify disk PARTUUID', default=None)
    umount_group.add_argument('--device-name', help='specify device name\n\n'+C.gBlue(), default=None)

    # - remount parser
    remount_parser=subparsers.add_parser("remount",
                        formatter_class=argparse.RawTextHelpFormatter,
                        help="remount process")
    remount_group=remount_parser.add_mutually_exclusive_group(required=True)
    remount_group.add_argument('--uuid', help='specify disk UUID', default=None)
    remount_group.add_argument('--partuuid', help='specify disk PARTUUID', default=None)
    remount_group.add_argument('--device-name', help='specify device name\n\n'+C.gBlue(), default=None)

    # - list parser
    list_parser=subparsers.add_parser("list",
                        formatter_class=argparse.RawTextHelpFormatter,
                        help="list devices (Default)\n\n")


    # -- add common options to all subparsers
    for name, subp in subparsers.choices.items():
        common_options(subp)


def post_process(args):
    # separazione degli args di tipo debug con quelli applicativi
    dbg=argparse.Namespace()
    log=argparse.Namespace()

    '''
    il processo che segue è per evitare:
       RuntimeError: dictionary changed size during iteration
       suddividiamo le varie options
    '''
    keys=list(args.__dict__.keys())
    # _dargs=args.__dict__
    for key in keys:
        val=getattr(args, key)
        if key in ['log']:
            setattr(log, key, val)
        elif key.startswith('log_'):
            setattr(log, key[4:], val)
        elif key.startswith('+log'):
            pass # le ignoro in quanto servono solo ad impostare il valore
        elif key in ['go', 'debug']:
            setattr(dbg, key, val)
        elif 'debug options' in key:
            pass
        elif 'log options' in key:
            pass
        else:
            continue

        delattr(args, key)

    app=args


    if args.display_args:
        del args.display_args
        import json
        json_data = json.dumps(vars(app), indent=4, sort_keys=True)
        print('application arguments: {json_data}'.format(**locals()))
        json_data = json.dumps(vars(log), indent=4, sort_keys=True)
        print('logging arguments: {json_data}'.format(**locals()))
        json_data = json.dumps(vars(dbg), indent=4, sort_keys=True)
        print('debugging arguments: {json_data}'.format(**locals()))
        sys.exit(0)

    return app, log, dbg

##############################################################
# - Parse Input
##############################################################
def parseInput(color=None):
    # global C
    # C=color

    # =============================================
    # = Parsing
    # =============================================
    if len(sys.argv) == 1: sys.argv.append('list')
    parser=argparse.ArgumentParser(
                description='Program to help mounting USB-disk on Raspberry (by: Ln)'+C.gYellow(),
                formatter_class=argparse.RawTextHelpFormatter)
    mainOptions(parser)

    args=parser.parse_args()
    return post_process(args)
