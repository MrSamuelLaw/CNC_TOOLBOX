#!/usr/bin/env

'''
runs test for local workbench
'''


import subprocess
import os
from lathe_parting import lathe_parting


def main():
    if False:
        subprocess.run("python -m unittest discover "+os.getcwd()+"\\test")
    if True:
        val = 250*12
        lp = lathe_parting().part('in', val, 1, .055)




if __name__ == "__main__":
    main()
