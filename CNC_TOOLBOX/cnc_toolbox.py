#!/usr/bin/env python


import pathlib
import os
import platform
import subprocess
from sys import argv


def main():
    cmd = list()
    # determine operating system so correct cmd is sent
    if platform.system() == 'Windows':
        cmd.append('pythonw')
    elif platform.system() == 'Linux':
        cmd.append('python3')
    # account for where program is called from
    folder = str(os.path.dirname(os.path.realpath(argv[0])))
    cmd.append(folder + "/__main__.py")
    cmd.append(folder)
    # if called with file to open as cmdline argument
    #   then open the file
    if len(argv) > 1:
        cmd.append(argv[1])
    # run the cmd with everything set correctly
    subprocess.run(cmd)



if __name__ == "__main__":
    main()
