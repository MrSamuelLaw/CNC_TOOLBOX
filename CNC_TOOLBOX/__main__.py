#!/usr/bin/env python


import os
import sys
import subprocess
import logging
import tools.sync_ui
if True:  # sync changes made using qt form designer
    tools.sync_ui.sync()
from my_mainwindow import *


def main():
    """
    setup logging and get cmdline arguments
    """

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

    if len(sys.argv) > 1:
        # if called from cnc_toolbox.py/exe externally
        # - argv[0] where the script was started from
        # - argv[1] exe directory
        # - argv[2] file to open's directory
        os.chdir(sys.argv[1])




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
    sys.exit(app.exec_())
