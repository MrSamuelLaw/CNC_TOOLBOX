#!/usr/bin/env python3


import os
import sys
import logging
import platform
from tendo import singleton
from tools import sync_ui
from PySide2 import QtGui, QtWidgets, QtCore
me = singleton.SingleInstance()  # prevent multiple instances of the app

# set config variables
SYNC_ON_STARTUP = True
STYLE = "dark"


def sync_ui_files():
    """
    calls the sync ui, which run the pyuic cmd
    on all ui files in the entire project
    """

    if SYNC_ON_STARTUP:
        sync_ui.sync()


def set_style(app):
    # see if there is a way to do this with
    # just style sheets, that way they can be
    # read into memory instead of set here
    """
    takes and app and style key and applies
    the given style to the entire app
    """

    if STYLE == 'dark':
        from PySide2.QtGui import QPalette, Qt, QColor
        # set dark style
        app.setStyle("Fusion")
        darkPalette = QPalette()
        darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.WindowText, Qt.white)
        darkPalette.setColor(QPalette.Base, QColor(25, 25, 25))
        darkPalette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
        darkPalette.setColor(QPalette.ToolTipText, Qt.white)
        darkPalette.setColor(QPalette.Text, Qt.white)
        darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ButtonText, Qt.white)
        darkPalette.setColor(QPalette.BrightText, Qt.red)
        darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(darkPalette)
        app.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a82da;
                border: 1px solid white;
            }
        """)


def load_icon(app, mainwindow):
    """
    takes an app and mainwindow instantiated
    in the if __name__ block and adds the icons
    located in the icons folder

    args:
        app: QtGui.QApplication
        mainwindow: QtGui.QMainwindow
    """

    icon = QtGui.QIcon()
    # common sizes used on different opperating systems
    icon.addFile('icon/icon16x16.png', QtCore.QSize(16, 16))
    icon.addFile('icon/icon24x24.png', QtCore.QSize(24, 24))
    icon.addFile('icon/icon32x32.png', QtCore.QSize(32, 32))
    icon.addFile('icon/icon48x48.png', QtCore.QSize(48, 48))
    icon.addFile('icon/icon256x256.png', QtCore.QSize(256, 256))
    app.setWindowIcon(icon)
    mainwindow.setWindowIcon(icon)
    # on windows supress python icon
    if platform.system() == 'Windows':
        import ctypes
        myappid = 'CNCTOOLBOX'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


def setup_logger():
    """
    creates a logger for this process with seperate
    console and file handlers
    """

    # set logger handle
    handle = 'log'
    logger = logging.getLogger(handle)
    logger.setLevel(level=logging.DEBUG)

    # define message format
    file_format = logging.Formatter(
        '%(levelname)s:'
        'func %(funcName)s:'
        'Line %(lineno)d:'
        '%(message)s'
    )
    console_format = logging.Formatter(
        '%(levelname)s:'
        '%(message)s'
    )

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


def main():
    """
    launches the app with the appropriate settings
    """

    setup_logger()

    # set cwd to where this script is located
    if len(sys.argv) > 1:
        # if called from cnc_toolbox.py/exe externally
        # - argv[0] where the script was started from
        # - argv[1] exe directory
        # - argv[2] file to open's directory
        os.chdir(sys.argv[1])

    sync_ui_files()  # sync ui before importings
    from my_mainwindow import my_mainwindow

    # load the app and mainwindow container
    app = QtWidgets.QApplication(sys.argv)
    set_style(app)
    mainwindow = QtWidgets.QMainWindow()

    # load mainwindow contents
    my_mainwindow(mainwindow)
    mainwindow.setWindowTitle("CNC TOOLBOX")
    load_icon(app, mainwindow)
    mainwindow.show()

    # run the program
    return_code = app.exec_()

    # clean up the pipe upon app ending
    with open('.pipe', 'w') as p:
        p.write('')

    # return exit status
    sys.exit(return_code)


if __name__ == "__main__":
    main()
