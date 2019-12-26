#!/usr/bin/env python


'''
module to run as admin in order to
install CNC TOOLBOX to the system

sudo code
- check if python is installed on the system

- create desktop shortcut with picture
- add cnc toolbox to path
'''

import sys
import os
import pkg_resources
import subprocess
from pkg_resources import DistributionNotFound, VersionConflict


def main():
    if int(sys.version[0]) == 3:
        met_code = 0
        dependencies = [
            'auto_py_to_exe',
            'PySide2',
        ]
        try:
            pkg_resources.require(dependencies)
            met_code = 1
        except Exception as e:
            met_code = 0
            for a in e.args:
                if a is not None:
                    print(a)
                    try:
                        p = subprocess.run([sys.executable, "-m", "pip", "install", str(a)])
                        met_code = 1
                    except Exception as e:
                        met_code = 0
                        print(e)
        if met_code:
            print('all depends met')

    else:
        print('please run with python3 not python2')


if __name__ == "__main__":
    main()
    input("Press <enter> to exit")
