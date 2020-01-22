#!/usr/bin/env python


import pathlib
import os
import platform
import subprocess
from sys import argv


def main():
    cmd = list()
    if platform.system() == 'Windows':
        # put in a bit here to search for venv is it exists
        cmd.append('pythonw')
    elif platform.system() == 'Linux':
        cmd.append('python3')
    folder = str(os.path.dirname(os.path.realpath(argv[0])))
    cmd.append(folder + "/__main__.py")
    cmd.append(folder)
    if len(argv) > 1:
        cmd.append(argv[1])
    subprocess.run(cmd)
    # e = subprocess.run(cmd)
    # print(e)
    # input("press <enter> to continue")


if __name__ == "__main__":
    main()
