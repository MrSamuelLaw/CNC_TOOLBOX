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
import site
import platform
import subprocess
import shutil


def linux_extra_sauce():
    linux_dependencies = [
            'xclip',
            'xsel'
    ]
    for d in linux_dependencies:
        try:
            p = subprocess.run(["which", str(d)])
            if p.returncode:
                try:
                    p = subprocess.run(['sudo', 'apt-get', 'install', str(d)])
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


def install_packages():
    if site.ENABLE_USER_SITE:
        dst = site.USER_SITE
        cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
        src = os.path.join(cwd,'packages/gscrape.py')
        try:
            shutil.copy(src, dst)
        except Exception as e:
            print(e)


def create_venv():
    pass
    # flesh out plan to create local venv and have
    # the program use it by default


def main():
    if int(sys.version[0]) == 3:  # make sure python3 is being used
        # put in dependencies
        dependencies = [
        'setuptools',
        'PySide2==5.13.0',
        'pyperclip'
        ]
        for d in dependencies:
            try:  # if not met install it
                p = subprocess.Popen([sys.executable, "-m", "pip", "install", str(d)], stdout=subprocess.PIPE)
                output = p.communicate()[0].decode('ASCII')
                if p.returncode:
                    print(output)
                else:
                    print(f'{d} requirement met')
            except Exception as e:
                print(e)

        # perform linux magic
        if platform.system() == 'Linux':
            linux_extra_sauce()
        # install gscrape
        install_packages()
    else:
        print('please run with python3 not python2')


if __name__ == "__main__":
    main()
    input("Press <enter> to exit")

