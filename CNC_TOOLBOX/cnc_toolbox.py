#!/usr/bin/env python


import pathlib
import os
import platform
import subprocess
import logging
from sys import argv


def main():
    """
    launch an instance of CNC_TOOLBOX
    """

    logger = logging.getLogger('log')
    cmd = list()
    # set cmd list based on operating system
    if platform.system() == 'Windows':
        logger.debug('platform is windows')
        cmd.append('pythonw')  # pythonw suppresses terminal
    elif platform.system() == 'Linux':
        logger.debug('platform is linux')
        cmd.append('python3')
    # account for where program is called from
    folder = str(os.path.dirname(os.path.realpath(argv[0])))
    cmd.append(os.path.join(folder, '__main__.py'))
    cmd.append(folder)
    # if called with file to open as cmdline argument then open the file
    if len(argv) > 1:
        cmd.append(argv[1])
    # run the cmd with everything set correctly
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
