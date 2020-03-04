#!/usr/bin/env python

from gui.mainwindow import *
from PySide2.QtWidgets import QFileDialog
from os import path
from collections import deque
from platform import system
import os
import sys
import logging


class my_mainwindow(Ui_MainWindow):

    _file = None
    _module = None

    def __init__(self, mainwindow):
        """
        set up main window
        """
        logging.info('setting up mainwindow')

        # setup to default screen
        self.setupUi(mainwindow)
        self.frame.hide()
        self.fnd_dockWidget.hide()

        # add functions
        self.menubar.addAction("open", self.launch_file_browser)
        self.menubar.addAction("close", self.close)
        self.menubar.addAction("save as", self.save_as)
        self.device_comboBox.currentIndexChanged.connect(self.load_workbench)
        self.save_button.clicked.connect(self.save_file)
        self.find_pushButton.clicked.connect(self.find)
        self.replace_pushButton.clicked.connect(self.replace)

        # add an additional function to the plainTextEdit
        #   that preserves the undo stack
        self.text_area.clearText = self.clearText

        # insert key bindings
        s1 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self.text_area)
        s1.activated.connect(self.fnd_dockWidget.show)

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

        logging.info('finished setting up mainwindow')

    def load_file(self):
        """
        open a file and puts its contents in the text area
        """
        self._file = sys.argv[2]
        self.file_field.setText(str(path.basename(self._file)))
        logging.info(f'loading file {str(path.basename(self._file))}')
        with open(self._file, 'r') as f:
            self.text_area.clear()
            self.text_area.insertPlainText(f.read())

    def launch_file_browser(self):
        '''
        launches a an instance of the os's native file browser
        to load a file into the text area
        '''
        logging.info('opening file browser')
        browser = QFileDialog()
        # browser.setNameFilter("nc files (*.nc)")  # filter if needed
        if browser.exec_():
            files = browser.selectedFiles()
            self._file = files[0]
            self.file_field.setText(str(path.basename(self._file)))
            with open(self._file, 'r') as f:
                self.text_area.clear()
                self.text_area.insertPlainText(f.read())

    def close(self):
        """
        close current file and wipe its contenst from the screen
        """
        self._file = None
        self.file_field.clear()
        self.text_area.clear()
        self.file_field.setText('no file selected')
        logging.info('file closed')

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
            self._file = files[0]
            self.file_field.setText(str(path.basename(self._file)))
            with open(self._file, 'w') as f:
                f.write(self.text_area.toPlainText())
        logging.info('file saved')

    def save_file(self):
        """
        save current file
        """
        if self._file is not None:
            file = self._file
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
        logging.info('file saved')

    def load_workbench(self):
        '''
        dynamically import a workbench from the wb folder.
        '''
        logging.info('loading workbench')
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
            logging.info('workbench loaded')

    def dynamic_import(self, mod_path, class_name):
        """
        dynamically import a specified module
        """
        # this is the code that makes the module import magic happen
        logging.debug('importing workbench module')
        self._module = __import__(mod_path, fromlist=[class_name])

    def del_all_in_layout(self, layout):
        """
        remove contents of a workbench from memory
        """
        logging.debug('deleting ui content from workbench')
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
        logging.debug('replacing frame')
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

    def clearText(self):
        """
        clear text while preserving the plainTextEdit's undo stack
        """
        logging.info('clearing text')
        # create a instance of a Q cursor with text doc as parent
        curs = QtGui.QTextCursor(self.text_area.document())
        # select all the content
        curs.select(QtGui.QTextCursor.Document)
        # delete all the content
        curs.deleteChar()
        curs.setPosition(0)

    def find(self):
        """
        find function for text area
        """
        text = self.find_lineEdit.text()  # string to find
        self.text_area.setFocus()  # ensures the text gets highlighted
        self.text_area.find(text)  # attempts to find the next instance

    def replace(self):
        """
        replace function for text area
        """
        new = self.replace_lineEdit.text()  # get new text
        self.text_area.textCursor().removeSelectedText()  # remove old
        self.text_area.textCursor().insertText(new)  # insert new
