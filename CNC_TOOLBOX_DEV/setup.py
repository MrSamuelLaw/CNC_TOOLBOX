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
import platform
import pkg_resources
import subprocess
from pkg_resources import DistributionNotFound, VersionConflict

'''
still need to make it install the packages
necessary for pyperclip to run
'''

def linux_extra_sauce():
    linux_dependencies = [
            'xclip',
            'xsel'
    ]
    for d in linux_dependencies:
        try:  # figure out how to run like in terminal
            p = subprocess.run(["which",str(d)])
            if p.returncode:
                try:
                    p = subprocess.run(['sudo', 'apt-get', 'install', str(d)])
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


def main():
    if int(sys.version[0]) == 3:  # make sure python3 is being used
        dependencies = [  # define depends
            'setuptools', 
            'PySide2',
            'pyperclip'
        ]
        for d in dependencies:
            try:
                if pkg_resources.require(d):  # check if met
                    print(d,' dependency is met') 
            except Exception as e:
                for a in list(filter(None, e.args)):
                    try:  # if not met install it
                        p = subprocess.run([sys.executable,
                                            "-m"
                                            "pip",
                                            "install",
                                            str(a)]
                                           )
                        if p.returncode == 0:
                            pass
                        else:
                            print(str(a),' may not have installed correctly')
                    except Exception as e:
                        print(e)
        if platform.system() == 'Linux':
            linux_extra_sauce()
    else:
        print('please run with python3 not python2')


if __name__ == "__main__":
    main()
    input("Press <enter> to exit")
