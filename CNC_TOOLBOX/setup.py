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
    installs the necessary linux packages to allow
    python packages to install correctly
    """

    major_ver, minor_ver, *_ = sys.version

    linux_dependencies = [
        'xclip',
        'xsel',
        f'python{major_ver}.{minor_ver}-venv'
    ]
    for d in linux_dependencies:
        try:
            # check if package exists
            p = subprocess.run(["which", str(d)])
            if p.returncode:
                try:
                    # try to install it
                    p = subprocess.run(['sudo', 'apt-get', 'install', str(d)])
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


def install_packages(install_path=None):
    """
    "install" (really just copy) gscrape.py. It's the heart of CNC toolbox that allows
    text to be turned into organized lists.
    """

    print('installing gscrape...')
    this_dir = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    dst = install_path
    src = os.path.join(this_dir, 'packages', 'gscrape.py')
    try:
        shutil.copy(src, dst)
    except Exception as e:
        print(e)
    else:
        print('gscrape installed successfully!')


def create_venv(cmd=None):
    """
    create a virtual enviroment for all the dependecies to be
    installed on
    """

    this_dir = str(os.path.dirname(os.path.realpath(sys.argv[0])))

    return_status = subprocess.run(cmd, cwd=this_dir)
    if return_status:
        print(return_status)
    elif not return_status:
        print('virtual enviroment created!')


def setup_windows():
    """
    runs the venv, and requirements setup for windows
    """
    print('setting up for windows...')

    create_venv(cmd=['python', '-m', 'venv', '.venv'])

    # install in dependencies
    print('installing required packages...')
    this_dir = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    cmd = ['./.venv/Scripts/pip3.exe', 'install', '-r', 'requirements.txt']
    return_status = subprocess.run(cmd, cwd=this_dir)
    print('packages installed with return stats:', return_status)

    # install gscrape
    dst = os.path.join(this_dir, '.venv', 'Lib', 'site-packages')
    install_packages(install_path=dst)


def setup_linux():
    """
    runs the venv, and requirements setup for windows
    """
    print('setting up for linux...')

    linux_extra_sauce()
    create_venv(cmd=['python3', '-m', 'venv', '.venv'])

    # install in dependencies
    print('installing required packages...')
    this_dir = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    cmd = ['./.venv/bin/pip3', 'install', '-r', 'requirements.txt']
    return_status = subprocess.run(cmd, cwd=this_dir)
    print('packages installed with the following status:', return_status)

    # install gscrape
    major_ver, minor_ver, *_ = sys.version
    dst = os.path.join(
        this_dir,
        '.venv',
        'lib',
        f'python{major_ver}.{minor_ver}',
        'site-packages'
    )
    install_packages(install_path=dst)


def main():
    """
    setup global enviroment for cnc_toolbox to run properly
    """

    if int(sys.version[0]) == 3:  # make sure python3 is being used
        if platform.system() == 'Linux':
            setup_linux()
        elif platform.system() == 'Windows':
            setup_windows()
    else:
        print('please run with python3 not python2')


if __name__ == "__main__":
    main()
    input("Press <enter> to exit")
