#!/usr/bin/env python

import os
import subprocess
import sync_ui
sync_ui.sync()


def main():
    if True:
        subprocess.run("python -m unittest discover "+os.getcwd()+"\\test")


if __name__ == "__main__":
    main()
