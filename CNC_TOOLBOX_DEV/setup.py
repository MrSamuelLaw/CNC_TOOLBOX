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

'''
still need to make it install the packages
necessary for pyperclip to run
'''

def main():
    if int(sys.version[0]) == 3:
    
        dependencies = [
            'setuptools',
            'PySide2',
            'pyperclip'
        ]
        for d in dependencies:
            try:
                pkg_resources.require(d)    
            except Exception as e:
                print(e)
                for a in e.args:
                    if a is not None:
                        print(a)
                        try:
                            p = subprocess.run([sys.executable,
                                                "-m"
                                                "pip",
                                                "install",
                                                str(a)]
                                              )
                            if p.returncode == 0:
                                print("successfully install {}".format(str(a)))     
                        except Exception as e:
                            print(e)
    else:
        print('please run with python3 not python2')


if __name__ == "__main__":
    main()
    input("Press <enter> to exit")
