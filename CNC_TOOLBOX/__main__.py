#!/usr/bin/env python


import os
import sys
import subprocess
import logging

# if singleton, go ahead and exit
from tendo import singleton
me = singleton.SingleInstance()

# sync ui prior to import
import tools.sync_ui
if True:
    tools.sync_ui.sync()
from my_mainwindow import *


def main():
    """
    setup logging and get cmdline arguments
    """

    # handle cmd line arguments
    if len(sys.argv) > 1:
        # if called from cnc_toolbox.py/exe externally
        # - argv[0] where the script was started from
        # - argv[1] exe directory
        # - argv[2] file to open's directory
        os.chdir(sys.argv[1])

# -----------------------------------------------------------------------
#    _____          _       _
#   / ____|        | |     | |
#  | (___     ___  | |_    | |        ___     __ _    __ _    ___   _ __
#   \___ \   / _ \ | __|   | |       / _ \   / _` |  / _` |  / _ \ | '__|
#   ____) | |  __/ | |_    | |____  | (_) | | (_| | | (_| | |  __/ | |
#  |_____/   \___|  \__|   |______|  \___/   \__, |  \__, |  \___| |_|
#                                             __/ |   __/ |
#                                            |___/   |___/
# ------------------------------------------------------------------------

    # set logger handle
    handle = 'log'
    logger = logging.getLogger(handle)
    logger.setLevel(level=logging.DEBUG)

    # define message format
    file_format = logging.Formatter('%(levelname)s:'
                                    'func %(funcName)s:'
                                    'Line %(lineno)d:'
                                    '%(message)s')
    console_format = logging.Formatter('%(levelname)s:'
                                       '%(message)s')

    # make seperate file and console output filters
    fh = logging.FileHandler('.log')
    fh.setLevel(level=logging.INFO)
    fh.setFormatter(file_format)
    ch = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG)
    ch.setFormatter(console_format)
    logger.addHandler(fh)
    logger.addHandler(ch)

    # clear the log file
    with open('.log', 'w') as f:
        f.write('')
        logger.debug('log cleared')


if __name__ == "__main__":
    main()  # call to collect cmd line arguments
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.startingUp()
    MainWindow = QtWidgets.QMainWindow()
    ui = my_mainwindow(MainWindow)
    MainWindow.setWindowTitle("CNC TOOLBOX")
    icon = QtGui.QIcon("icon/logo.png")
    MainWindow.setWindowIcon(icon)
    MainWindow.show()
    return_code = app.exec_()
    # clean up the pipe
    with open('.pipe', 'w') as p:
        p.write('')
    sys.exit(return_code)


