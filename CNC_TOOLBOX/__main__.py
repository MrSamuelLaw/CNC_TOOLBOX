#!/usr/bin/env python3


import os
import sys
import logging
import platform
from tendo import singleton
from tools import sync_ui
from PySide2 import QtGui, QtWidgets, QtCore
me = singleton.SingleInstance()

# set ui syncing status
SYNC_ON_STARTUP = True


def sync_ui_files():
    if SYNC_ON_STARTUP:
        sync_ui.sync()


def set_style(app, style):
    if style == 'dark':
        from PySide2.QtGui import QPalette, Qt, QColor
        # set dark style
        app.setStyle("Fusion")
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(dark_palette)
        app.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a82da;
                border: 1px solid white;
            }
        """)


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


if __name__ == "__main__":
    main()  # call to collect cmd line arguments
    sync_ui_files()
    from my_mainwindow import my_mainwindow

    app = QtWidgets.QApplication(sys.argv)
    set_style(app, 'dark')

    mainwindow = QtWidgets.QMainWindow()
    my_mainwindow(mainwindow)
    mainwindow.setWindowTitle("CNC TOOLBOX")
    # different sizes for different computers
    icon = QtGui.QIcon()
    icon.addFile('icon/icon16x16.png', QtCore.QSize(16, 16))
    icon.addFile('icon/icon24x24.png', QtCore.QSize(24, 24))
    icon.addFile('icon/icon32x32.png', QtCore.QSize(32, 32))
    icon.addFile('icon/icon48x48.png', QtCore.QSize(48, 48))
    icon.addFile('icon/icon256x256.png', QtCore.QSize(256, 256))

    # on windows supress python icon
    if platform.system() == 'Windows':
        import ctypes
        myappid = 'CNCTOOLBOX'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app.setWindowIcon(icon)
    mainwindow.setWindowIcon(icon)
    mainwindow.show()

    return_code = app.exec_()
    # clean up the pipe
    with open('.pipe', 'w') as p:
        p.write('')

    sys.exit(return_code)
