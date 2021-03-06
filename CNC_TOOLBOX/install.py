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
import platform as pf
import subprocess


def install_linux_packages(platform: str):
    if platform == 'Linux':
        # get the packages from packages.txt
        with open('packages.txt', 'r') as inFile:
            packages = inFile.readlines()
            packages = [x.strip() for x in packages]

        # ask the user if they want the script to install them
        print("attempting to install the following linux packages:")
        for p in packages:
            print(p)
        print("you may be prompted to enter your password...")
        # try and install the linux packages
        try:
            subprocess.run(['sudo', 'apt-get', 'update'])
            for p in packages:
                # try to install it
                return_status = subprocess.run(['sudo', 'apt-get', 'install', str(p)])
                print(return_status)
        except Exception as e:
            print(e, '\n', return_status)
        else:
            print("finished installing linux packages...")
    else:
        raise ValueError(f'{platform} is not "Linux"')


def create_virtual_enviroment(platform: str, path: str):
    # WINDOWS
    if platform == 'Windows':
        cmd = ['python', '-m', 'venv', '.venv']

    # LINUX
    elif platform == 'Linux':
        cmd = ['python3', '-m', 'venv', '.venv']

    # NOT LINUX OR WINDOWS
    else:
        raise ValueError(f'{platform} is not "Windows" or "Linux"')

    print("creating virtual environment...")
    try:
        return_status = subprocess.run(cmd, cwd=path)
    except Exception as e:
        print(e, '\n', return_status)
    else:
        print(return_status)
        print('virtual enviroment created!')


def install_python_packages(platform: str, path: str):

    skips = ['.venv']
    requirements = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if (name == "requirements.txt"):  # loop through and find test folders
                file_ = os.path.join(root, name)
                # make sure files are not in directories to skip
                if not any([s for s in skips if s in file_]):
                    requirements.append(file_)

    # WINDOWS
    if platform == 'Windows':
        exe = './.venv/Scripts/pip3.exe'

    # LINUX
    elif platform == 'Linux':
        exe = './.venv/bin/pip3'

    # NOT LINUX OR WINDOWS
    else:
        raise ValueError(f'{platform} is not "Windows or "Linux"')

    print('installing required python packages...')
    try:
        for req in requirements:
            cmd = [exe, 'install', '-r', req]
            return_status = subprocess.run(cmd, cwd=path)
        cmd = [exe, 'install', './packages']
        return_status = subprocess.run(cmd, cwd=path)
    except Exception as e:
        print(e, '\n', return_status)
    else:
        print('packages installed')


def setup():
    """
    runs the venv, and requirements setup for windows
    """

    platform = pf.system()
    print(f"setting up for {platform}")
    this_dir = str(os.path.dirname(os.path.realpath(sys.argv[0])))
    # install linux packages
    if platform == 'Linux':
        install_linux_packages(platform)

    # create virtual enviroment
    create_virtual_enviroment(platform, this_dir)

    # install python packages
    install_python_packages(platform, this_dir)


def main():
    """
    setup global enviroment for cnc_toolbox to run properly
    """

    if int(sys.version_info.major) == 3:  # make sure python3 is being used
        setup()
    else:
        print('please run with python3 not python2')


if __name__ == "__main__":
    main()
    input("Press <enter> to exit")
