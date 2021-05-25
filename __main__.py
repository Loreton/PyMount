#!/usr/bin/python
#
# #############################################
#
# updated by ...: Loreto Notarantonio
# Date .........: 2021-05-25
#
# #############################################

import  sys; sys.dont_write_bytecode = True
import  os
from    pathlib import Path
this=sys.modules[__name__]
from types import SimpleNamespace


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
                        null_log=log.no_log,
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
        'force': args.force,
        'execute': dbg.go,
    }
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


    dev_uuid=my_dev['uuid']
    cfg_dev=myConfig['UUIDS'].get(dev_uuid)

    # ########### MOUNT
    if args.action=='mount':
        DisplayDevice.display(my_dev, msg=f'current status {args.action}')
        dev=SimpleNamespace(**my_dev)

        if dev.mounted:

            if dev.mountpoint==cfg_dev['mountpoint']:
                msg = f"device {dev.path} is already and correctly mounted on: {dev.mountpoint}"
                logger.info(msg)
                C.pYellowH(text=msg, tab=4)
                # rCode=0

            elif args.force:
                rCode=MountUmount.umount(my_dev, fEXECUTE=dbg.go, my_logger=logger)
                if rCode==0:
                    my_dev=DeviceList.getDevice(config=myConfig['UUIDS'], myLogger=logger, **dev_kwargs)
                    rCode=MountUmount.mount(my_dev, fEXECUTE=dbg.go, my_logger=logger)
                    my_dev=DeviceList.getDevice(config=myConfig['UUIDS'], myLogger=logger, **dev_kwargs)
                    DisplayDevice.display(my_dev, msg='status after mount')
                else:
                    logger.error("Error mounting device", my_dev, exit=True)
            else:
                msg = f"""device {dev.path}
                is already mounted on: {dev.mountpoint}
                but it's different from required mountpoint: {cfg_dev["mountpoint"]}
                use '--force' to modify it"""
                # C.pRedH(text=msg, tab=4)
                logger.error(msg, exit=True, console=True)

        else:
            rCode=MountUmount.mount(my_dev, fEXECUTE=dbg.go, my_logger=logger)



    # ########### UMOUNT
    elif args.action=='umount':
        DisplayDevice.display(my_dev, msg=f'current status {args.action}')
        rCode=MountUmount.umount(my_dev, fEXECUTE=dbg.go, my_logger=logger)



    # if rCode==0 and dbg.go:
    #     my_dev=DeviceList.getDevice(config=myConfig['UUIDS'], myLogger=logger, **dev_kwargs)
    #     DisplayDevice.display(my_dev, msg=f'status after {args.action}')

    print ()
    print ()
    sys.exit()

