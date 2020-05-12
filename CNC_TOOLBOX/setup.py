#!/usr/bin/env python3


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
import platform
import subprocess
import shutil


def linux_extra_sauce():
    """
    adds the linux distros necessary for copy and paste functionality
    """

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
    """
    "install" (really just copy) gscrape.py. It's the heart of CNC toolbox that allows
    text to be turned into organized lists.
    """

    print('installing gscrape...')
    this_dir = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    # dst = './.venv/Lib/site-packages'
    dst = os.path.join(this_dir, '.venv', 'Lib', 'site-packages')
    src = os.path.join(this_dir, 'packages', 'gscrape.py')
    try:
        shutil.copy(src, dst)
    except Exception as e:
        print(e)
    else:
        print('gscrape installed successfully!')


def create_venv():
    """
    create a virtual enviroment for all the dependecies to be
    installed on
    """

    this_dir = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    cmd = ['python', '-m', 'venv', '.venv']
    return_status = subprocess.run(cmd, cwd=this_dir)
    if return_status:
        print('.venv already exists...')
    elif not return_status:
        print('virtual enviroment created!')


def main():
    """
    setup global enviroment for cnc_toolbox to run properly
    """

    if int(sys.version[0]) == 3:  # make sure python3 is being used
        # create virtual enviroment
        print('creating virtual enviroment...')
        create_venv()


        # install in dependencies
        print('installing required packages...')
        this_dir = str(os.path.dirname(os.path.realpath(sys.argv[0])))
        cmd = ['./.venv/Scripts/pip3.exe', 'install', '-r', 'requirements.txt']
        return_status = subprocess.run(cmd, cwd=this_dir)
        print('packages installed with return stats:', return_status)

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
