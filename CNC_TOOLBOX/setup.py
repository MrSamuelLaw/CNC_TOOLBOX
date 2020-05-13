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


def setup_windows():
    """
    runs the venv, and requirements setup for windows
    """

    print("setting up for windows...")

    # create virtual enviroment
    print("creating virtual environment...")
    this_dir = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    cmd = ['python', '-m', 'venv', '.venv']
    return_status = subprocess.run(cmd, cwd=this_dir)
    if return_status:
        print(return_status)
    elif not return_status:
        print('virtual enviroment created!')

    # install python packages
    print('installing required python packages...')
    cmd = ['./.venv/Scripts/pip3.exe', 'install', '-r', 'requirements.txt']
    return_status = subprocess.run(cmd, cwd=this_dir)
    print('packages installed')

    # install gscrape
    print('installing gscrape...')
    src = os.path.join(this_dir, 'packages', 'gscrape.py')
    dst = os.path.join(
        this_dir, '.venv', 'Lib', 'site-packages')
    try:
        shutil.copy(src, dst)
    except Exception as e:
        print(e)
    else:
        print('gscrape installed successfully!')


def setup_linux():
    """
    runs the venv, and requirements setup for linux
    """

    # install linux dependencies
    print('setting up for linux...')

    # get the packages from packages.txt
    major_ver = sys.version_info.major
    minor_ver = sys.version_info.minor
    with open('packages.txt', 'r') as inFile:
        packages = inFile.readlines()
        packages = [x.strip() for x in packages]
        # for i, p in enumerate(packages):
        #     if p == 'python{major_ver}.{minor_ver}-venv':
        #         packages[i] = p.format(major_ver=major_ver, minor_ver=minor_ver)

    # ask the user if they want the script to install them
    print("attempting to install the following linux packages:")
    for p in packages:
        print(p)
    print("you may be prompted to enter your password...")
    for p in packages:
        # try to install it
        p = subprocess.run(['sudo', 'apt-get', 'install', str(p)])
        print(p)
    # excecption not caught on purpose, we don't want the
    # program to continue if an error occures
    print("finished installing linux packages...")

    # create virtual enviroment
    print("creating virtual environment...")
    this_dir = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    cmd = ['python3', '-m', 'venv', '.venv']
    return_status = subprocess.run(cmd, cwd=this_dir)
    if return_status:
        print(return_status)
    elif not return_status:
        print('virtual enviroment created!')

    # install python packages
    print('installing required python packages...')
    cmd = ['./.venv/bin/pip3', 'install', '-r', 'requirements.txt']
    return_status = subprocess.run(cmd, cwd=this_dir)
    print('packages installed')

    # install gscrape
    print('installing gscrape...')
    src = os.path.join(this_dir, 'packages', 'gscrape.py')
    dst = os.path.join(
        this_dir, '.venv', 'lib', 'python{}.{}'.format(major_ver, minor_ver), 'site-packages'
    )
    try:
        shutil.copy(src, dst)
    except Exception as e:
        print(e)
    else:
        print('gscrape installed successfully!')


def main():
    """
    setup global enviroment for cnc_toolbox to run properly
    """

    if int(sys.version_info.major) == 3:  # make sure python3 is being used
        if platform.system() == 'Linux':
            setup_linux()
        elif platform.system() == 'Windows':
            setup_windows()
    else:
        print('please run with python3 not python2')


if __name__ == "__main__":
    main()
    input("Press <enter> to exit")
