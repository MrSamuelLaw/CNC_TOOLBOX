#!/usr/bin/env python


import os
import subprocess
from glob import glob


def sync():
    """
    finds all .ui files and calls PySide2-uic on them
    which converts them to .py files
    """

    ext = '*.ui'
    files = []
    start_dir = os.getcwd()

    for fpath, _, _ in os.walk(start_dir):
        files.extend(glob(os.path.join(fpath, ext)))
    for f in files:
        ui = f
        py = f[0:-3]+'.py'
        cmd = ["pyside2-uic", ui, '-o', py]
        subprocess.run(cmd, shell=True)  # shell prevents popup window
