#!/usr/bin/python
# -*- coding: utf-8 -*-

# updated by ...: Loreto Notarantonio
# Date .........: 2021-06-27
#
import sys, os
from pathlib import Path

'''
# permette di fare l'import senza passare le subdirs
from    lnLib.setPathsLN import setPaths; setPaths(sub_dirs=[
                                                'Source',
                                                'Source/Security',
                                                'lnLib',
                                                ],
                                                fDEBUG=False)
'''




# permette di fare l'import senza passare le subdirs
def setPaths(sub_dirs=[], fDEBUG=False):
    # check if I'm inside a ZIP file or directory
    thisScript=Path(sys.argv[0]).resolve()
    script_path=thisScript.parent # ... then up one level

    my_path=[]
    if thisScript.suffix == '.zip': # potrei essere anche all'interno dello zip
        prj_main_dir=thisScript.parent.parent
        my_path.append(thisScript)
        my_path.extend(extractZip(thisScript)) # extract lnLib.zip from project.zip file and get its path
        script_path=thisScript # ... change it to ... up one level
    else:
        prj_main_dir=script_path

    my_path.append(prj_main_dir)
    for dir_name in sub_dirs:
        my_path.append(Path(script_path / dir_name))

    for item in my_path:
        sys.path.insert(0, str(item))
        if fDEBUG:
            print ('    ', item)


    return prj_main_dir



import zipfile
# from io import BytesIO

def extractZip(zipFilename):
    zip_paths=[]
    with zipfile.ZipFile(zipFilename, 'r') as zipObj:
       nameList = zipObj.namelist()
       for fileName in nameList:
           # Check filename endswith csv
           if fileName.endswith('.zip'):
               # Extract a single file from zip
               _path=zipObj.extract(fileName, path='/tmp/lnpython')
               zip_paths.append(_path)

    return zip_paths

import re, io
def extractZip_inZip(filename):
    zip_path=[]
    with zipfile.ZipFile(filename, 'r') as zfile:
        for name in zfile.namelist():
            if re.search(r'\.zip$', name) != None:
                zfiledata = io.BytesIO(zfile.read(name))
                _name=Path(name).parts[-1] # get only fname.zip
                _path=write_bytesio_to_file(fname=_name, bytesio=zfiledata, destdir='/tmp/lnpython')
                zip_path.append(_path)
                continue
                # extract files in zip2 if necessary
                with zipfile.ZipFile(zfiledata) as zfile2:
                    for name2 in zfile2.namelist():
                        print(name2)

    return zip_path


def write_bytesio_to_file(*, fname, bytesio, destdir):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet. 
    """
    filepath=Path(destdir).joinpath(fname)
    # os.makedirs(os.path.dirname(filepath),  exist_ok=True)
    os.makedirs(destdir,  exist_ok=True)
    with open(filepath, "wb") as fout:
        # Copy the BytesIO stream to the output file
        fout.write(bytesio.getbuffer())
    return filepath