#!/usr/bin/env python

import logging
import os
import threading
from time import sleep
from PySide2 import QtCore, QtGui, QtWidgets
from gui.mainwindow import Ui_MainWindow
from gui.splitTabWidget import splitViewTabWidget


# -------------------------------------------------------
#   _        _         _
#  | |      (_)       | |
#  | |       _   ___  | |_    ___   _ __     ___   _ __
#  | |      | | / __| | __|  / _ \ | '_ \   / _ \ | '__|
#  | |____  | | \__ \ | |_  |  __/ | | | | |  __/ | |
#  |______| |_| |___/  \__|  \___| |_| |_|  \___| |_|
# -------------------------------------------------------


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


# -----------------------------------------------------------------------------------
#                       _                      _               _
#                      (_)                    (_)             | |
#   _ __ ___     __ _   _   _ __   __      __  _   _ __     __| |   ___   __      __
#  | '_ ` _ \   / _` | | | | '_ \  \ \ /\ / / | | | '_ \   / _` |  / _ \  \ \ /\ / /
#  | | | | | | | (_| | | | | | | |  \ V  V /  | | | | | | | (_| | | (_) |  \ V  V /
#  |_| |_| |_|  \__,_| |_| |_| |_|   \_/\_/   |_| |_| |_|  \__,_|  \___/    \_/\_/
# ------------------------------------------------------------------------------------


class my_mainwindow(Ui_MainWindow):

    _module = None
    toolbar_padding = 5

    def __init__(self, mainwindow):
        """
        set up main window
        """

        # set up logger
        self._logger = logging.getLogger('log')
        self._logger.info('setting up mainwindow')

        # # set up listener
        self.listener = Listener()
        self.listener.signals.heard.connect(self.open)
        self.thread = threading.Thread(target=self.listener.run)
        self.thread.daemon = True
        self.thread.start()

        # start document count at zero
        self.d_count = 0

        # setup to default screen
        self.setupUi(mainwindow)
        self.bottomToolBar.hide()
        self.splitView = splitViewTabWidget()
        self.splitView.twd['right'].hide()
        self.cw_gridLayout.replaceWidget(self.placeHolder, self.splitView)

        # create statusbar at the bottom of the screen
        self.setup_status_bar(mainwindow)

        # override drag and drop functions for central widget
        self.centralwidget.setAcceptDrops(True)
        self.centralwidget.dragEnterEvent = self.dragEnterEvent
        self.centralwidget.dropEvent = self.dropEvent

        # set up toolbars
        self.toolBar.addWidget(self.toolbar_widget)
        self.toolBar.setMinimumHeight(
            self.toolbar_widget.height() + self.toolbar_padding
        )
        self.wb_toolbar = QtWidgets.QToolBar('wb_toolbar')
        self.wb_widget = None
        self.bottomToolBar.addWidget(self.findReplaceWidget)

        # setup file menu
        self.filemenu = self.menubar.addMenu("file")
        self.filemenu.addAction("new", self.open)
        self.filemenu.addAction("open", self.browse)
        self.filemenu.addAction("save", self.save)
        self.filemenu.addAction("save as", self.save_as)

        # connect signals and slots
        self.device_comboBox.currentIndexChanged.connect(self.load_workbench)
        self.find_pushButton.clicked.connect(self.find)
        self.replace_pushButton.clicked.connect(self.replace)
        self.splitView.signals.focusChanged.connect(self.set_current_document_id)
        self.hideButton.clicked.connect(self.bottomToolBar.hide)

        # setup hotkeys
        s1 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self.splitView)
        s1.activated.connect(self.bottomToolBar.show)
        s2 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+s"), self.splitView)
        s2.activated.connect(self.save)

        # load the wb combo box
        self.device_comboBox.addItem('start menu')
        self.wb_list = os.listdir(os.getcwd() + '/wb')
        for wb in self.wb_list:
            if wb != 'info.txt':
                self.device_comboBox.addItem(wb)

        self._logger.info('finished setting up mainwindow')

    # -------------------------------------------------------------------
    #    _____   _             _                   ____
    #   / ____| | |           | |                 |  _ \
    #  | (___   | |_    __ _  | |_   _   _   ___  | |_) |   __ _   _ __
    #   \___ \  | __|  / _` | | __| | | | | / __| |  _ <   / _` | | '__|
    #   ____) | | |_  | (_| | | |_  | |_| | \__ \ | |_) | | (_| | | |
    #  |_____/   \__|  \__,_|  \__|  \__,_| |___/ |____/   \__,_| |_|
    # -------------------------------------------------------------------

    def setup_status_bar(self, mainwindow):
        # create new widget
        status_widget = QtWidgets.QWidget(mainwindow)
        # create layout
        layout = QtWidgets.QHBoxLayout()
        # create spacer to push text all the way to the right
        spacer = QtWidgets.QSpacerItem(
            2000,  # width
            0,  # height
            QtWidgets.QSizePolicy.Expanding,  # width policy
            QtWidgets.QSizePolicy.Minimum  # height policy
        )
        layout.addSpacerItem(spacer)
        # create status label that self can change
        self.stat_label = QtWidgets.QLabel('', mainwindow)
        # put label into layout
        layout.addWidget(self.stat_label)
        # apply layout to status widget
        status_widget.setLayout(layout)
        mainwindow.statusBar().addWidget(status_widget)

    def set_statusbar_right_text(self, text):
        self.stat_label.setText(f'current: {text}')

    # ---------------------------------------------------------------------------------------
    #   ______   _   _               _    _                       _   _   _
    #  |  ____| (_) | |             | |  | |                     | | | | (_)
    #  | |__     _  | |   ___       | |__| |   __ _   _ __     __| | | |  _   _ __     __ _
    #  |  __|   | | | |  / _ \      |  __  |  / _` | | '_ \   / _` | | | | | | '_ \   / _` |
    #  | |      | | | | |  __/      | |  | | | (_| | | | | | | (_| | | | | | | | | | | (_| |
    #  |_|      |_| |_|  \___|      |_|  |_|  \__,_| |_| |_|  \__,_| |_| |_| |_| |_|  \__, |
    #                                                                                  __/ |
    #                                                                                 |___/
    # ---------------------------------------------------------------------------------------

    def get_current_plainTextEdit(self):
        return self.splitView.getPlainTextEdit(
            self._current_document_id
        )

    def set_current_document_id(self, _id):
        """ catches the current item _id emitted
        by the split view widget the _id is how the
        splitViewWidget is able to find items"""

        self._logger.info(f'current item is {_id}')
        self._current_document_id = _id
        self.set_statusbar_right_text(_id)

    def browse(self):
        """
        use file browser to select file
        """

        self._logger.info('opening file browser')
        browser = QtWidgets.QFileDialog()
        if browser.exec_():
            files = browser.selectedFiles()
            tf = files[0]
            self.open(filepath=tf)

    def open(self, filepath=None):
        """
        open a new tab and load contents
        """

        if filepath is not None:
            # put the contents on a new tab
            with open(filepath, 'r') as c:
                contents = c.read()
                # set the tab title
                title = os.path.basename(filepath)
                self._logger.info(f'opening {title}')
                self.splitView.openTextDocument(
                    title,
                    contents,
                    filepath=filepath
                )
        else:
            self._logger.info('opening blank tab')
            self.splitView.openTextDocument(f'document{self.doc_count()}')

    def close(self, index=None):
        """
        close current file and wipe its contents from the screen
        """
        self.splitView.closeTab()

    def save(self):
        """
        save a file using the appropriate method
        """
        item_info = self.splitView.getItemInfo(
            self._current_document_id
        )
        if item_info['path'] is None:
            self.save_as()
        elif self.copy_radio.isChecked():
            self.save_copy()
        elif self.overwrite_radio.isChecked():
            self.save_overwrite()

    def save_overwrite(self):
        self._logger.info('saving file')
        item_info = self.splitView.getItemInfo(
            self._current_document_id
        )
        contents = str(item_info['doc'].toPlainText())
        with open(item_info['path'], 'w') as f:
            f.write(contents)

    def save_copy(self):
        self._logger.info('saving file copy')
        item_info = self.splitView.getItemInfo(
            self._current_document_id
        )
        contents = item_info['doc'].toPlainText()
        file_name = 'copy_' + os.path.basename(item_info['path'])
        dirpath = os.path.dirname(item_info['path'])
        with open(os.path.join(dirpath, file_name), 'w') as f:
            f.write(contents)

    def save_as(self):
        """
        save the current contents to a new file
        """

        self._logger.info('saving file as')
        browser = QtWidgets.QFileDialog()
        # optional settings that allow consistent saving accross platforms
        options = browser.Options()
        options |= browser.DontUseNativeDialog
        options |= browser.DontUseCustomDirectoryIcons
        browser.setLabelText(browser.Accept, 'Save')
        browser.setOptions(options)
        if browser.exec_():
            files = browser.selectedFiles()
            tf = files[0]
            # get the document associated with tab that has Focus
            item_info = self.splitView.getItemInfo(self._current_document_id)
            # get the file path
            item_info['path'] = tf
            item_info['id'] = str(os.path.basename(tf))
            # update item _id and thus title
            self.splitView.updateItem(
                self._current_document_id,
                item_info['id']
            )
            self._current_document_id = item_info['id']
            # write contents to file
            with open(tf, 'w') as f:
                content = str(item_info['doc'].toPlainText())
                f.write(content)

            self._logger.info(f'{tf} saved')

    # --------------------------------------------------------------------------
    #   _____                                    _____
    #  |  __ \                           ___    |  __ \
    #  | |  | |  _ __    __ _    __ _   ( _ )   | |  | |  _ __    ___    _ __
    #  | |  | | | '__|  / _` |  / _` |  / _ \/\ | |  | | | '__|  / _ \  | '_ \
    #  | |__| | | |    | (_| | | (_| | | (_>  < | |__| | | |    | (_) | | |_) |
    #  |_____/  |_|     \__,_|  \__, |  \___/\/ |_____/  |_|     \___/  | .__/
    #                            __/ |                                  | |
    #                           |___/                                   |_|
    # ---------------------------------------------------------------------------

    def dragEnterEvent(self, e):
        """
        filters drag events
        """
        # check if item being dragged in has a path or not
        self._logger.debug('dragEnterEvent detected')
        if e.mimeData().hasUrls():
            e.accept()  # if has path, allow drops

    def dropEvent(self, e):
        """
        filters drop events
        """
        # if okayed by the dragEnterEvent
        self._logger.debug('dropEvent detected')
        for url in e.mimeData().urls():
            p = str(url.toLocalFile())
            if os.path.isfile(p):
                self.open(p)

    # ----------------------------------------------------------------------------
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
    # ----------------------------------------------------------------------------

    def load_workbench(self):
        '''
        dynamically import a workbench from the wb folder.
        '''

        if self.device_comboBox.currentIndex() == 0:
            # close wb_toolbar
            self.wb_toolbar.clear()
            self.wb_toolbar.hide()
            if self.wb_widget is not None:
                # delete widget from memory
                self.wb_widget.deleteLater()
            # set selfs attributes to none
            self.wb_widget = None
            self._wb = None

        else:
            self.wb_widget = QtWidgets.QWidget()
            self._logger.info('loading workbench')
            self.wb_toolbar.clear()  # clear the wb_toolbar
            # dynamically import wb based on device selection
            # this is the reason that the naming convention is important
            if self.wb_widget is not None:
                old = self.wb_widget
                old.deleteLater()
                self.wb_widget = QtWidgets.QWidget()
            device = self.device_comboBox.currentText()
            class_name = ''.join(['my_', device, '_wb'])
            mod_path = ''.join(['wb.', device, '.', class_name])
            self.dynamic_import(mod_path, class_name)
            wb = getattr(self._module, class_name)()
            self._wb = wb.run_integrated(self)  # self it parent
            # so that the child workbench can pull the elements
            # necessary for its opperation
            # self.frame = self._wb.frame
            self.wb_toolbar.addWidget(self._wb.wb_widget)
            self.get_parent().addToolBarBreak()
            self.get_parent().addToolBar(self.wb_toolbar)
            self.wb_toolbar.show()
            self._logger.info('workbench loaded')

    def dynamic_import(self, mod_path, class_name):
        """
        dynamically import a specified module
        """

        # this is the code that makes the module import magic happen
        self._logger.debug('importing workbench module')
        self._module = __import__(mod_path, fromlist=[class_name])

    # -----------------------------------------------------------------------
    #                       __  __   _
    #                      |  \/  | (_)
    #                      | \  / |  _   ___    ___
    #                      | |\/| | | | / __|  / __|
    #                      | |  | | | | \__ \ | (__
    #                      |_|  |_| |_| |___/  \___|
    # -----------------------------------------------------------------------

    def find(self):
        """
        find function for text area find & replace
        """

        text = self.find_lineEdit.text()  # string to find
        self._logger.debug(f'searching text for {text}')
        item = self.splitView._currentItem  # be careful using currentItem
        item.setFocus()  # ensures the text gets highlighted
        item.find(text)  # attempts to find the next instance

    def replace(self):
        """
        replace function for text area find & replace
        """

        new = self.replace_lineEdit.text()  # get new text
        self._logger.debug(f'replacement text is {new}')
        item = self.splitView._currentItem
        item.textCursor().removeSelectedText()  # remove old
        item.textCursor().insertText(new)  # insert new

    def doc_count(self):
        self.d_count += 1
        return self.d_count

    def get_parent(self):
        return self.centralwidget.parentWidget()
