#!/usr/bin/env python


'''
main script from which the unit testing will be performed
'''
import os
import sys
import subprocess
from my_mainwindow import *


def main():
    if len(sys.argv) > 1:
        # if run externally
        # - argv[0] where the script was started from
        # - argv[1] exe directory
        # - argv[2] file to open's directory
        os.chdir(sys.argv[1])


if __name__ == "__main__":
    main()
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
