#!/usr/bin/env python

import logging
import os
import sys
import threading
import asyncio
from os import path
from time import sleep
from platform import system
from PySide2.QtWidgets import QFileDialog
from gui.mainwindow import *


#-------------------------------------------------------
#   _        _         _
#  | |      (_)       | |
#  | |       _   ___  | |_    ___   _ __     ___   _ __
#  | |      | | / __| | __|  / _ \ | '_ \   / _ \ | '__|
#  | |____  | | \__ \ | |_  |  __/ | | | | |  __/ | |
#  |______| |_| |___/  \__|  \___| |_| |_|  \___| |_|
#-------------------------------------------------------


class ListenerSignals(QtCore.QObject):
    heard = QtCore.Signal(str)


class Listener(QtCore.QObject):

    def __init__(self):
        self._logger = logging.getLogger('log')
        self.signals = ListenerSignals()

    def get_line(self, pipe):
        return pipe.readline().strip()

    def run(self):
        with open('.pipe', 'r') as pipe:
            while True:
                line = pipe.readline().strip()
                if len(line):
                    self.signals.heard.emit(line)
                sleep(0.7)


#-----------------------------------------------------------------------------------
#                       _                      _               _
#                      (_)                    (_)             | |
#   _ __ ___     __ _   _   _ __   __      __  _   _ __     __| |   ___   __      __
#  | '_ ` _ \   / _` | | | | '_ \  \ \ /\ / / | | | '_ \   / _` |  / _ \  \ \ /\ / /
#  | | | | | | | (_| | | | | | | |  \ V  V /  | | | | | | | (_| | | (_) |  \ V  V /
#  |_| |_| |_|  \__,_| |_| |_| |_|   \_/\_/   |_| |_| |_|  \__,_|  \___/    \_/\_/
#------------------------------------------------------------------------------------


class my_mainwindow(Ui_MainWindow):

    _module = None

    def test_func(self, stuff):
        print(stuff)

    def __init__(self, mainwindow):
        """
        set up main window
        """

        # set up logger
        self._logger = logging.getLogger('log')
        self._logger.info('setting up mainwindow')

        # # clear the pipe
        # with open('.pipe', 'w') as pipe:
        #     pipe.write('')

        # # set up a subthread
        self.listener = Listener()
        self.listener.signals.heard.connect(self.open)
        self.thread = threading.Thread(target=self.listener.run)
        self.thread.daemon = True
        self.thread.start()

        # start document count at zero
        self.d_count = 0

        # setup to default screen
        self.setupUi(mainwindow)
        self.frame.hide()
        self.fnd_dockWidget.hide()

        # set up the tabbed widget
        self.new_tab()
        self.text_area = self.tabWidget.currentWidget().text_area
        self.tabWidget.tabCloseRequested.connect(self.close)

        # add functions
        self.filemenu = self.menubar.addMenu("file")
        self.filemenu.addAction("new", self.new)
        self.filemenu.addAction("open", self.browse)
        self.filemenu.addAction("close", self.close)
        self.filemenu.addAction("save", self.save)
        self.filemenu.addAction("save as", self.save_as)
        self.tabWidget.currentChanged.connect(self.set_tab)
        self.device_comboBox.currentIndexChanged.connect(self.load_workbench)

        self.find_pushButton.clicked.connect(self.find)
        self.replace_pushButton.clicked.connect(self.replace)

        # load the wb combo box
        self.device_comboBox.addItem('start menu')
        self.wb_list = os.listdir(os.getcwd()+'/wb')
        for wb in self.wb_list:
            if wb != 'info.txt':
                self.device_comboBox.addItem(wb)

        # load in a file if passed as command line
        if len(sys.argv) > 2:
            if os.path.isfile(sys.argv[2]):
                try:
                    self.load_file()
                except Exception as e:
                    print(e)

        self._logger.info('finished setting up mainwindow')

#---------------------------------------------------------------------------------------
#   ______   _   _               _    _                       _   _   _
#  |  ____| (_) | |             | |  | |                     | | | | (_)
#  | |__     _  | |   ___       | |__| |   __ _   _ __     __| | | |  _   _ __     __ _
#  |  __|   | | | |  / _ \      |  __  |  / _` | | '_ \   / _` | | | | | | '_ \   / _` |
#  | |      | | | | |  __/      | |  | | | (_| | | | | | | (_| | | | | | | | | | | (_| |
#  |_|      |_| |_|  \___|      |_|  |_|  \__,_| |_| |_|  \__,_| |_| |_| |_| |_|  \__, |
#                                                                                  __/ |
#                                                                                 |___/
#---------------------------------------------------------------------------------------

    def new(self):
        """
        opens a new tab without contents
        """

        self._logger.info('opening a new tab')
        self.open()

    def browse(self):
        """
        use file browser to select file
        """

        self._logger.info('opening file browser')
        browser = QFileDialog()
        if browser.exec_():
            files = browser.selectedFiles()
            tf = files[0]
            self.open(filepath=tf)

    def open(self, filepath=None):
        """
        open a new tab and load contents
        """

        tab = self.new_tab()
        if filepath is not None:
            # set the tab filepath
            tab._file = filepath
            # put the contents on a new tab
            with open(filepath, 'r') as c:
                contents = c.read()
                tab.text_area.insertPlainText(str(contents))
            # set the tab title
            index = self.tabWidget.indexOf(tab)
            title = os.path.basename(filepath)
            self.tabWidget.setTabText(index, title)
        else:
            # open a blank tab
            self.tabWidget.setCurrentWidget(tab)
        # set view to new tab
        self.tabWidget.setCurrentWidget(tab)

    def close(self, index=None):
        """
        close current file and wipe its contents from the screen
        """

        if index is None:  # close tab with focus
            tab = self.tabWidget.currentWidget()
            self.close_tab(tab)
            self._logger.info('file closed')
        else: # signal came from tabCloseRequested
            tab = self.tabWidget.widget(index)
            self.close_tab(tab)
            self._logger.info('file closed')

    def save(self):
        """
        save a file using the appropriate method
        """

        if self.copy_radio.isChecked():
            self.save_copy()
        elif self.overwrite_radio.isChecked():
            self.save_overwrite()

    def save_overwrite(self):
        self._logger.info('saving file')
        tab = self.tabWidget.currentWidget()
        contents = tab.text_area.toPlainText()
        with open(tab._file, 'w') as f:
            f.write(contents)

    def save_copy(self):
        self._logger.info('saving file copy')
        tab = self.tabWidget.currentWidget()
        contents = tab.text_area.toPlainText()
        file_name = 'copy_'+os.path.basename(tab._file)
        dirpath = os.path.dirname(tab._file)
        with open(os.path.join(dirpath, file_name), 'w') as f:
            f.write(contents)

    def save_as(self):
        """
        save the current contents to a new file
        """

        self._logger.info('saving file as')
        browser = QFileDialog()
        # patch to allow the save as to work on linux
        if system() == 'Linux':
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            options |= QFileDialog.DontUseCustomDirectoryIcons
            browser.setLabelText(QtWidgets.QFileDialog.Accept, 'Save')
            browser.setOptions(options)
        if browser.exec_():
            files = browser.selectedFiles()
            tf = files[0]
            self.tabWidget.currentWidget()._file = tf
            with open(tf, 'w') as f:
                f.write(self.text_area.toPlainText())
            self.tabWidget.setTabText(self.tabWidget.currentIndex(),
                                      str(path.basename(tf)))
        self._logger.info(f'{tf} saved')

#---------------------------------------------------------------------------------------------------------
#   _______           _           __  __                                                              _
#  |__   __|         | |         |  \/  |                                                            | |
#     | |      __ _  | |__       | \  / |   __ _   _ __     __ _    __ _   _ __ ___     ___   _ __   | |_
#     | |     / _` | | '_ \      | |\/| |  / _` | | '_ \   / _` |  / _` | | '_ ` _ \   / _ \ | '_ \  | __|
#     | |    | (_| | | |_) |     | |  | | | (_| | | | | | | (_| | | (_| | | | | | | | |  __/ | | | | | |_
#     |_|     \__,_| |_.__/      |_|  |_|  \__,_| |_| |_|  \__,_|  \__, | |_| |_| |_|  \___| |_| |_|  \__|
#                                                                   __/ |
#                                                                  |___/
#---------------------------------------------------------------------------------------------------------

    def set_tab(self):
        try:
            self.text_area = self.tabWidget.currentWidget().text_area
        except Exception as e:
            self._logger.warning(str(e))

    def new_tab(self):
        self._logger.info('creating new tab')
        new_tab = QtWidgets.QTabWidget(self.tabWidget)

        new_tab.grid_layout = QtWidgets.QGridLayout(new_tab)
        new_tab.grid_layout.setContentsMargins(0, 0, 0, 0)
        new_tab.grid_layout.setObjectName("grid_layout")

        new_tab.text_area = QtWidgets.QPlainTextEdit(new_tab)

        # add an additional function to the plainTextEdit
        #   that preserves the undo stack
        new_tab.text_area.clearText = self.clearText

        # tabs keep track of the files they have open
        new_tab._file = None

        # insert key bindings
        s1 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), new_tab.text_area)
        s1.activated.connect(self.fnd_dockWidget.show)
        s2 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+s"), new_tab.text_area)
        s2.activated.connect(self.save)

        # add to layout
        new_tab.grid_layout.addWidget(new_tab.text_area, 0, 0, 1, 1)
        self.tabWidget.addTab(new_tab, f'untitled {self.doc_count()}')

        return new_tab

    def close_tab(self, tab):
        self._logger.info('closing tab')
        try:
            self.del_all_in_layout(tab.grid_layout)
            tab.deleteLater()
        except Exception as e:
            logging.warning(str(e))

#----------------------------------------------------------------------------
#  __          __                 _      _                             _
#  \ \        / /                | |    | |                           | |
#   \ \  /\  / /    ___    _ __  | | __ | |__     ___   _ __     ___  | |__
#    \ \/  \/ /    / _ \  | '__| | |/ / | '_ \   / _ \ | '_ \   / __| | '_ \
#     \  /\  /    | (_) | | |    |   <  | |_) | |  __/ | | | | | (__  | | | |
#   __ \/_ \/      \___/  |_|    |_|\_\ |_.__/   \___| |_| |_|  \___| |_| |_|
#   __  __                                                              _
#  |  \/  |                                                            | |
#  | \  / |   __ _   _ __     __ _    __ _   _ __ ___     ___   _ __   | |_
#  | |\/| |  / _` | | '_ \   / _` |  / _` | | '_ ` _ \   / _ \ | '_ \  | __|
#  | |  | | | (_| | | | | | | (_| | | (_| | | | | | | | |  __/ | | | | | |_
#  |_|  |_|  \__,_| |_| |_|  \__,_|  \__, | |_| |_| |_|  \___| |_| |_|  \__|
#                                     __/ |
#                                    |___/
#----------------------------------------------------------------------------

    def load_workbench(self):
        '''
        dynamically import a workbench from the wb folder.
        '''

        if self.device_comboBox.currentIndex() == 0:
            # reset frame if no device selected
            if self.frame.layout() is not None:
                # clear all the widgets out of frame so
                # they don't stay in memory
                self.del_all_in_layout(self.frame.layout())
                # que the layout for deletion since it will not
                # be needed since we are returning to
                # the start menu
                self.frame.layout().deleteLater()
                self.frame.hide()
                self._wb = None
        else:
            self._logger.info('loading workbench')
            if self.frame.layout() is not None:
                self.del_all_in_layout(self.frame.layout())
                self.replace_frame()
            # dynamically import wb based on device selection
            # this is the reason that the naming convention is important
            device = self.device_comboBox.currentText()
            class_name = 'my_'+device+'_wb'
            mod_path = 'wb.'+device+'.'+class_name
            self.dynamic_import(mod_path, class_name)
            wb = getattr(self._module, class_name)()
            self._wb = wb.run_integrated(self)  # self it parent
            # so that the child workbench can pull the elements
            # necessary for its opperation
            self.frame = self._wb.frame
            self.frame.show()
            self._logger.info('workbench loaded')

    def dynamic_import(self, mod_path, class_name):
        """
        dynamically import a specified module
        """

        # this is the code that makes the module import magic happen
        self._logger.debug('importing workbench module')
        self._module = __import__(mod_path, fromlist=[class_name])

    def del_all_in_layout(self, layout):
        """
        remove contents of a workbench from memory
        """

        self._logger.debug('deleting ui content from layout')
        # this code removes everything from a layout
        # prior to deletion to prevent memory leaks
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.del_all_in_layout(layout)

    def replace_frame(self):
        """
        provide new frame for wb to fill if old one has not
        been deleted from memory
        """

        self._logger.debug('replacing frame')
        # capture the parent
        p = self.frame.parent()

        # capture frame position
        for i in range(self.gridLayout.count()):
            type_ = str(self.gridLayout.itemAt(i).widget())
            if 'QFrame' in type_:  # Make sure it is a QFrame
                # row, col, rowspan, colspan
                r, c, rs, cs = self.gridLayout.getItemPosition(i)

        # delete frame widget
        self.del_all_in_layout(self.gridLayout)

        # the code below is modified from the
        # file created py the pyuic that turns ui files
        # into python files.

        # replace the old frame that is now qued for deletion
        self.frame = QtWidgets.QFrame(p)  # put parent
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        # add it back into the layout
        self.gridLayout.addWidget(self.frame, r, c, rs, cs)

#-----------------------------------------------------------------------
#                       __  __   _
#                      |  \/  | (_)
#                      | \  / |  _   ___    ___
#                      | |\/| | | | / __|  / __|
#                      | |  | | | | \__ \ | (__
#                      |_|  |_| |_| |___/  \___|
#-----------------------------------------------------------------------

    def clearText(self):
        """
        clear text while preserving the plainTextEdit's undo stack
        """

        self._logger.info('clearing text')
        # create a instance of a Q cursor with text doc as parent
        curs = QtGui.QTextCursor(self.text_area.document())
        # select all the content
        curs.select(QtGui.QTextCursor.Document)
        # delete all the content
        curs.deleteChar()
        curs.setPosition(0)

    def find(self):
        """
        find function for text area find & replace
        """

        text = self.find_lineEdit.text()  # string to find
        self._logger.debug(f'searching text for {text}')
        self.text_area.setFocus()  # ensures the text gets highlighted
        self.text_area.find(text)  # attempts to find the next instance

    def replace(self):
        """
        replace function for text area find & replace
        """

        new = self.replace_lineEdit.text()  # get new text
        self._logger.debug(f'replacement text is {new}')
        self.text_area.textCursor().removeSelectedText()  # remove old
        self.text_area.textCursor().insertText(new)  # insert new

    def doc_count(self):
        self.d_count += 1
        return self.d_count
