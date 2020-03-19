#!/usr/bin/env python

import logging
import os
import sys
from collections import deque
from os import path
from platform import system

from PySide2.QtWidgets import QFileDialog

from gui.mainwindow import *


class my_mainwindow(Ui_MainWindow):

    _module = None

    def __init__(self, mainwindow):
        """
        set up main window
        """

        self._logger = logging.getLogger('log')
        self._logger.info('setting up mainwindow')
        self.d_count = 0

        # setup to default screen
        self.setupUi(mainwindow)
        self.frame.hide()
        self.fnd_dockWidget.hide()

        # set up the tabbed widget
        self.new_tab()
        self.text_area = self.tabWidget.currentWidget().text_area
        self.tabWidget.tabCloseRequested.connect(self.close_tab)

        # add functions
        self.filemenu = self.menubar.addMenu("file")
        self.filemenu.addAction("new", self.new_tab)
        self.filemenu.addAction("open", self.open_file)
        self.filemenu.addAction("close", self.close)
        self.filemenu.addAction("save", self.save_file)
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

    def load_file(self):
        """
        open a file and puts its contents in the text area
        """

        self.tabWidget.currentWidget()._file = sys.argv[2]  # get path to file
        tf = self.tabWidget.currentWidget()._file
        self._logger.info(f'loading file {str(path.basename(tf))}')
        # set tab title
        self.tabWidget.setTabText(self.tabWidget.currentIndex(),
                                  str(path.basename(tf)))
        # put contents on the screen
        with open(tf, 'r') as f:
            self.text_area.insertPlainText(f.read())

    def open_file(self):
        '''
        launches a an instance of the os's native file browser
        to load a file into the text area
        '''

        self._logger.info('opening file browser')
        browser = QFileDialog()
        # browser.setNameFilter("nc files (*.nc)")  # filter if needed
        if browser.exec_():
            files = browser.selectedFiles()
            tf = files[0]

            # if no tabs exist
            if self.tabWidget.currentIndex() < 0:
                self.new_tab()
                t_index = self.tabWidget.currentIndex()
            # if tab exists and has no content in the text area
            elif not len(self.tabWidget.currentWidget().text_area.toPlainText()):
                self.text_area = self.tabWidget.currentWidget().text_area
                t_index = self.tabWidget.currentIndex()
            # if tab exists and has content in it
            else:
                self.new_tab()
                t_index = self.tabWidget.currentIndex() + 1
                self.tabWidget.setCurrentIndex(t_index)
                self.text_area = self.tabWidget.widget(t_index).text_area

            # update title
            self.tabWidget.widget(t_index)._file = tf
            self.tabWidget.setTabText(t_index, str(path.basename(tf)))
            with open(tf, 'r') as f:
                self.text_area.clear()
                self.text_area.insertPlainText(f.read())

    def close(self):
        """
        close current file and wipe its contenst from the screen
        """

        self.text_area.clear()
        self._logger.info('file closed')

    def save_as(self):
        """
        save the current contents to a new file
        """

        logging.info('saving file as')
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

    def save_file(self):
        """
        save current file
        """
        tf = self.tabWidget.currentWidget()._file
        if tf is not None:
            file = tf
            if self.save_copy.isChecked():
                folder = path.dirname(file)
                file_name = 'fixed_'+path.basename(file)
                file = folder+'/'+file_name
                with open(file, 'w+') as f:
                    f.write(self.text_area.toPlainText())
            else:
                with open(file, 'w+') as f:
                    f.write(self.text_area.toPlainText())

        else:
            self.save_as()
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
        s2.activated.connect(self.save_file)

        # add to layout
        new_tab.grid_layout.addWidget(new_tab.text_area, 0, 0, 1, 1)
        self.tabWidget.addTab(new_tab, f'untitled {self.doc_count()}')

    def close_tab(self):
        self._logger.info('closing tab')
        try:
            current_tab = self.tabWidget.currentWidget()
            self.del_all_in_layout(current_tab.grid_layout)
            current_tab.deleteLater()
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
