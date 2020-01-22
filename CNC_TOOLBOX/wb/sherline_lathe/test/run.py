#!/usr/bin/env

'''
runs test for local workbench
'''


import subprocess
import os


def main():
    if True:
        subprocess.run("python -m unittest discover "+os.getcwd()+"/test")


if __name__ == "__main__":
    main()
