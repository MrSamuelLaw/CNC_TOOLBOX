#!/usr/bin/env python


import os
import subprocess
from glob import glob


def sync():
    ext = '*.ui'
    files = []
    start_dir = os.getcwd()

    for fpath, _, _ in os.walk(start_dir):
        files.extend(glob(os.path.join(fpath, ext)))
    for f in files:
        if (f.find('"') == -1):
            f = '"'+f+'"'
            cmd = "pyside2-uic "+f+' -o '+f[0:-3]+'py" -x'
            subprocess.run(cmd)
