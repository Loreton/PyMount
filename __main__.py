#!/usr/bin/python
#
# #############################################
#
# updated by ...: Loreto Notarantonio
# Date .........: 2021-05-24
#
# #############################################

import  sys; sys.dont_write_bytecode = True
import  os
from    pathlib import Path
this=sys.modules[__name__]


# permette di fare l'import senza passare le subdirs
from    Source.lnLib.setPathsLN import setPaths; setPaths(sub_dirs=[
                                                'Source',
                                                'Source/lnLib',
                                                'Source/lnLib/colorama_043',
                                                'Source/Main',
                                                ],
                                                fDEBUG=False)


from  loggerLN                import getLogger
from  parseInput              import parseInput
from  configurationLoaderLN   import Main as LoadConfigFile
# from  resolveDictVarsLN       import ResolveDictVars


from toYaml                    import readYamlFile, writeYamlFile, print_dict


# import types # for SimpleNamespace()

# from LnLib.yamlLoaderLN import loadYamlFile
# from LnLib.loggerLN     import setLogger
# from LnLib.promptLN     import prompt
# from LnLib              import monkeyPathLN # necessario per i miei comandi di Path (tra cui file.sizeRotate())


# from Source.parseInputLN import parseInput
import DeviceList
import DisplayDevice; display=DisplayDevice.display
# from Source import MountUmount


def get_my_dev(config, args, all_devices=False, fPRINT=False):
    req_mpoint=args.mpoint if 'mpoint' in args else None
    device_list=DeviceList.deviceList(config, req_mpoint=req_mpoint)

    if all_devices:
        logger.debug('DEVICES found:', device_list)
        if fPRINT:
            for name, _device in device_list.items():
                DisplayDevice.display(_device, msg='current status')
            print()
        return device_list

    logger.info('DEVICE required:', args)
    for name, my_dev in device_list.items():

        _device=SimpleNamespace(**my_dev)

        args_name=getattr(args, 'name', None)
        args_uuid=getattr(args, 'uuid', None)
        args_partuuid=getattr(args, 'partuuid', None)

        if name==args_name or _device.uuid==args_uuid or _device.partuuid==args_partuuid:
            logger.info('DEVICE found:', my_dev)
            return my_dev

    logger.warning('NO DEVICE found:')
    return None





######################################
# sample call:
#
######################################
if __name__ == '__main__':

    print('starting....')
    _this_filepath=Path(sys.argv[0]).resolve()
    script_path=_this_filepath.parent # ... then up one level
    prj_name=script_path.stem
    log_dir=f'/tmp/{prj_name}'

    """ parsing input --------------- """
    args, log, dbg=parseInput()
    """ parsing end --------------- """




    """ logger ---------------"""
    logger=getLogger(   logger_name='pyMount',
                        configuration_file=Path("conf/logger_config.yaml"),
                        log_filename=Path(f'{log_dir}/{prj_name}.log'),
                        console_level=log.console,
                        exclude_modules=log.exclude,
                        include_modules=log.include,
                    )

    """ logger start ----------- """
    logger.info('application arguments:', vars(args))
    logger.debug('logging arguments:', log)
    logger.debug('debugging arguments:', vars(dbg))
    """ logger end ------------- """



    ''' read Main configuration file '''
    logger.info('loading configuration file:', 'conf/main_config.yaml')

    os.environ['script_path']=str(script_path) # potrebbe essere usata nel config_file
    myConfig=LoadConfigFile(f'conf/{prj_name.lower()}_config.yaml')
    # print_dict(myConfig)

    # ----
    if args.action=='list':
        device_list=get_my_dev(myConfig['UUIDs'], args, all_devices=True, fPRINT=True)
        sys.exit()





    kwargs={
        'my_logger': logger,
        'configuration_data': myConfig
    }


    import pdb; pdb.set_trace() # by Loreto


    prj_dir=Path(sys.argv[0]).resolve().parent

    '''
        Questo step serve per quando siamo all'interno dello zip
        anche se, per non incorrere in errori,
        mi conviene impostare il nome staticamente
    '''
    if prj_dir.stem=='bin': prj_dir=prj_dir.parent
    prj_name=prj_dir.stem
    prj_name='pymount'

    os.environ['Prj_Name']=prj_name # potrebbe usarla loadYamlFile()

    ''' read Main configuration file '''
    dConfig=loadYamlFile(f'conf/{prj_name}.yml', resolve=True, fPRINT=False)

    ''' parsing input (return Namespace data)'''
    args, inp_log, dbg=parseInput(color=C)

    ''' logger '''
    log=dConfig['logger']
    log['filename']=f'/tmp/{prj_name}.log'


    #- override configuration logger with input parameters
    if inp_log.console: log['console']=inp_log.console
    if inp_log.modules: log['modules']=inp_log.modules
    if inp_log.level: log['level']=inp_log.level


    logger = setLogger(log)

    logger.debug3('input   arguments', args.__dict__)
    logger.debug3('logging arguments', inp_log)
    logger.debug3('debug   arguments', dbg.__dict__)
    logger.debug3('configuration data', dConfig)
    # -------------------------------
    gv.logger=logger
    gv.TAB='   [Ln]: '


    # ---- inizializzazione di alcuni moduli che utilizzano i global values...
    _myGlobal={'logger': logger, 'color': LnColor()}
    prompt(gVars=_myGlobal)
    MountUmount.setup(gVars=_myGlobal)
    DisplayDevice.setup(gVars=_myGlobal)
    # ----
    if args.action=='list':
        device_list=get_my_dev(dConfig['UUIDs'], args, all_devices=True, fPRINT=True)
        sys.exit()

    # ---- legge i device disponibili (lsblk)
    my_dev=get_my_dev(dConfig['UUIDs'], args)
    if not my_dev:
        C.pError(text='Required device was NOT found', tab=4)
        sys.exit()


    if args.action=='mount':
        display(my_dev, msg=f'status before {args.action}')
        rCode=MountUmount.mount(my_dev, fEXECUTE=dbg.go)

    elif args.action=='umount':
        display(my_dev, msg=f'status before {args.action}')
        rCode=MountUmount.umount(my_dev, fEXECUTE=dbg.go)

    elif args.action=='remount':
        display(my_dev, msg=f'status before {args.action}')
        rCode=MountUmount.umount(my_dev, fEXECUTE=dbg.go)
        if rCode==0:
            my_dev=get_my_dev(dConfig['UUIDs'], args) # re-read device status
            rCode=MountUmount.mount(my_dev, fEXECUTE=dbg.go)





    # display(my_dev, msg=f'status after {args.action}')
    #- display current status
    # print(rCode)
    if rCode==0:
        my_dev=get_my_dev(dConfig['UUIDs'], args)
        display(my_dev, msg=f'status after {args.action}')

    msg = "     program completed."
    print ()
    print (msg)
    print ()
