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

from colorLN import LnColor; C=LnColor()
import DisplayDevice
import DeviceList
import MountUmount

# from toYaml                    import readYamlFile, writeYamlFile, print_dict






######################################
# sample call:
#
######################################
if __name__ == '__main__':

    print('starting....')
    _this_filepath=Path(sys.argv[0]).resolve()
    script_path=_this_filepath.parent # ... then up one level
    prj_name='PyMount'
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

    dev_kwargs={
        'name': getattr(args, 'name', None),
        'uuid': getattr(args, 'uuid', None),
        'label': getattr(args, 'label', None),
        'partuuid': getattr(args, 'partuuid', None),
    }

    # ----
    if args.action=='list':
        # ---- legge i device disponibili (lsblk)
        device_list=DeviceList.deviceList(config=myConfig['UUIDS'], myLogger=logger, fPRINT=True)
        sys.exit()

    my_dev=DeviceList.getDevice(config=myConfig['UUIDS'], myLogger=logger, **dev_kwargs)
    if not my_dev:
        C.pError(text='Required device was NOT found', tab=4)
        sys.exit()



    if args.action=='mount':
        DisplayDevice.display(my_dev, msg=f'current status {args.action}')
        rCode=MountUmount.mount(my_dev, fEXECUTE=dbg.go, my_logger=logger)

    elif args.action=='umount':
        DisplayDevice.display(my_dev, msg=f'current status {args.action}')
        rCode=MountUmount.umount(my_dev, fEXECUTE=dbg.go, my_logger=logger)

    elif args.action=='remount':
        DisplayDevice.display(my_dev, msg=f'current status {args.action}')
        rCode=MountUmount.umount(my_dev, fEXECUTE=dbg.go, my_logger=logger)
        if rCode==0:
            my_dev=DeviceList.getDevice(config=myConfig['UUIDS'], myLogger=logger, **dev_kwargs) # re-read device status
            rCode=MountUmount.mount(my_dev, fEXECUTE=dbg.go, my_logger=logger)



    if rCode==0 and dbg.go:
        my_dev=DeviceList.getDevice(config=myConfig['UUIDS'], myLogger=logger, **dev_kwargs)
        DisplayDevice.display(my_dev, msg=f'status after {args.action}')

    print ()
    print ()
    sys.exit()

