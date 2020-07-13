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
    """
    signals for the listener thread

    protected attributes
        _heard: a QtCore.Signal that emits a python str
    """

    heard = QtCore.Signal(str)


class Listener(QtCore.QObject):
    """
    class that runs on a seperate thread in order to process
    file open requests from cnc_toolbox.py and cnc_toolbox.exe

    public functions:
        run():
            starts a thread that runs for the life of the mainwindow
            that processes file open requests that come from seperate
            processes.

        signals:
            heard.emit(str): emits line from pipe if available
    """

    def __init__(self):
        """
        creates a logger and adds signals through
        composition
        """

        self.logger = logging.getLogger('log')
        self.signals = ListenerSignals()

    def run(self):
        """
        listens to the .pipe for opening files to
        open
        """

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
    """
    front end for CNC_TOOLBOX

    description:
        my_mainwindow inherites from the auto-generated file mainwindow.py, which itself
        is generated from mainwindow.ui
        The purpose of this class is to handle all the base functionality of CNC_TOOLBOX
        as well as to host submodules in its wb_toolbar.

    ascii art website:
        http://patorjk.com/software/taag/#p=display&f=Big&t=F%20i%20l%20e%20%20%20%20%20%20H%20a%20n%20d%20l%20i%20n%20g

    class structure
        due to the many tasks the my_mainwindow handles
        the functions have been split into catagories defined
        by ascii block text, here are the brief overviews of the catagories
        Setup:
            everything that must be done for the mainwindow to
            start correctly and called by the __init__ function
        File Handling:
            everything related to opening, closing, and saving text
        Drag&Drop:
            overwrites drag and drop handling for the central widget,
            thus allowing files to be dragged, dropped, and opened
        Workbench Management:
            everything that has to do with importing, displaying, and
            memory managing the workbench modules
        Misc:
            functions that are not important enough to have their
            own section, like find and replace, etc...
    """

    _module = None
    toolbar_padding = 1

    def __init__(self, mainwindow):
        """
        set up main window
        """

        # set up logger
        self.logger = logging.getLogger('log')
        self.logger.info('setting up mainwindow')

        # set up listener
        self.start_listener_thread()
        # start document count at zero
        self.d_count = 0
        # setup to default screen
        self.customize_mainwindow(mainwindow)
        # create statusbarWidget at the bottom of the screen
        self.setup_status_bar(mainwindow)
        # override drag and drop functions for central widget
        self.enable_drag_n_drop()
        # set up toolbars
        self.setup_toolbars()
        # setup file menu
        self.create_file_menu()
        # connect signals and slots
        self.connect_signals_and_slots()
        # setup hotkeys
        self.assign_hotkeys()
        # load the wb combo box
        self.load_device_combobox()

        self.logger.info('finished setting up mainwindow')

    # -------------------------------------
    #   _____          _
    #  / ____|        | |
    # | (___     ___  | |_   _   _   _ __
    #  \___ \   / _ \ | __| | | | | | '_ \
    #  ____) | |  __/ | |_  | |_| | | |_) |
    # |_____/   \___|  \__|  \__,_| | .__/
    #                             | |
    #                             |_|
    # -------------------------------------

    def start_listener_thread(self):
        """
        starts the listener thread to pole the .pipe
        for file open requests
        """

        self.listener = Listener()
        self.listener.signals.heard.connect(self.open)
        self.thread = threading.Thread(target=self.listener.run)
        self.thread.daemon = True
        self.thread.start()

    def customize_mainwindow(self, mainwindow):
        """
        customizes the mainwindow in ways that
        cannot be done in Qt-Designer
        """

        self.setupUi(mainwindow)
        self.bottomToolBar.hide()
        self.splitView = splitViewTabWidget()
        self.splitView.twd['right'].hide()
        self.cw_gridLayout.replaceWidget(self.placeHolder, self.splitView)

    def create_file_menu(self):
        """
        creates the filemenu located in the top left
        of the mainwindow
        """

        self.filemenu = self.menubar.addMenu("file")
        self.filemenu.addAction("new", self.open)
        self.filemenu.addAction("open", self.browse)
        self.filemenu.addAction("save", self.save)
        self.filemenu.addAction("save as", self.save_as)

    def connect_signals_and_slots(self):
        """
        connect QSignals and QSlots
        """

        self.device_comboBox.currentIndexChanged.connect(self.load_workbench)
        self.find_pushButton.clicked.connect(self.find)
        self.replace_pushButton.clicked.connect(self.replace)
        self.splitView.signals.focusChanged.connect(self.set_current_document_id)
        self.hideButton.clicked.connect(self.bottomToolBar.hide)

    def assign_hotkeys(self):
        """
        assigns and enables hotkeys
        """

        s1 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self.splitView)
        s1.activated.connect(self.bottomToolBar.show)
        s2 = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+s"), self.splitView)
        s2.activated.connect(self.save)

    def enable_drag_n_drop(self):
        """
        modifies and/or overwrites drag and drop behavior
        """

        self.centralwidget.setAcceptDrops(True)
        self.centralwidget.dragEnterEvent = self.dragEnterEvent
        self.centralwidget.dropEvent = self.dropEvent

    def setup_toolbars(self):
        """
        creates the workbench toolbar
        """

        self.toolBar.addWidget(self.toolbarWidget)
        self.toolBar.setMinimumHeight(
            self.toolbarWidget.height() + self.toolbar_padding
        )
        self.wb_toolbar = QtWidgets.QToolBar('wb_toolbar')
        self.wb_widget = None
        self.bottomToolBar.addWidget(self.findReplaceWidget)

    def load_device_combobox(self):
        """
        reads the available devices in the wb folder
        and loads them into the combo box
        """

        self.device_comboBox.addItem('start menu')
        self.wb_list = os.listdir(os.getcwd() + '/wb')
        for wb in self.wb_list:
            if wb != 'info.txt':
                self.device_comboBox.addItem(wb)

    def setup_status_bar(self, mainwindow):
        """
        adds a label to the bottom right status bar
        """

        # create status label that self can change
        self.stat_label = QtWidgets.QLabel('', mainwindow)
        # add to the right of the mainwindow
        mainwindow.statusBar().addPermanentWidget(self.stat_label)

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
        """
        returns the currently active document's plainTextEdit
        """

        return self.splitView.getPlainTextEdit(
            self._current_document_id
        )

    def set_current_document_id(self, _id):
        """
        catches the current item _id emitted
        by the splitViewTabWidget
        the _id is how the
        splitViewTabWidget is able to find items
        """

        self.logger.info(f'current item is {_id}')
        self._current_document_id = _id
        self.set_statusbar_right_text(_id)
        self.get_current_plainTextEdit().setFocus()

    def browse(self):
        """
        opens a file browser to select a file using
        the operating systems native file browser
        """

        self.logger.info('opening file browser')
        browser = QtWidgets.QFileDialog()
        if browser.exec_():
            files = browser.selectedFiles()
            tf = files[0]
            self.open(filepath=tf)

    def open(self, filepath=None, title=None):
        """
        opens a new tab in the splitViewTabWidget

        args:
            filepath
                if=None, simply opens a new tab
                if != None, reads file contents onto new tab
        """

        if filepath is not None:
            # put the contents on a new tab
            with open(filepath, 'r') as c:
                contents = c.read()
                # set the tab title
                title = os.path.basename(filepath)
                self.logger.info(f'opening {title}')
                self.splitView.openTextDocument(
                    title,
                    text=contents,
                    filepath=filepath
                )
        elif title is not None:
            self.splitView.openTextDocument(title)

        else:
            self.logger.info('opening blank tab')
            self.splitView.openTextDocument(f'document{self.doc_count}')

    def close(self, index=None):
        """
        calls the closeTab method of the splitViewTabWidget to
        close the current tab.
        """

        self.splitView.closeTab()

    def save(self):
        """
        saves the tabs contents
        if there is a path associated with file implements
        save copy or save overwrite methods
        if there is no path, falls through to save as method
        """

        item_info = self.splitView.getItemInfo(
            self._current_document_id
        )
        if item_info['path'] is None:
            self.save_as()
        elif self.copy_radioButton.isChecked():
            self.save_copy()
        elif self.overwrite_radioButton.isChecked():
            self.save_overwrite()

    def save_overwrite(self):
        """
        overwrites the contents of a file with the text
        in the current tab, iff there is a path associated
        with the tab, else it calls save_as()
        """

        self.logger.info('saving file')
        item_info = self.splitView.getItemInfo(
            self._current_document_id
        )
        contents = str(item_info['doc'].toPlainText())
        with open(item_info['path'], 'w') as f:
            f.write(contents)

    def save_copy(self):
        """
        saves the contents of the current tab as a copy
        with a modified name iff there is a path associated
        with the tab, else it calls save_as()
        """

        self.logger.info('saving file copy')
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
        save the current contents to a new file using
        a save as dialog window
        """

        self.logger.info('saving file as')
        browser = QtWidgets.QFileDialog()

        # optional settings that allow consistent saving accross platforms
        options = browser.Options()
        options |= browser.DontUseNativeDialog
        options |= browser.DontUseCustomDirectoryIcons
        browser.setLabelText(browser.Accept, 'Save')
        browser.setOptions(options)

        if browser.exec_():
            # get the path that you just created
            File, *_ = browser.selectedFiles()

            # get the document associated with tab that has Focus
            item_info = self.splitView.getItemInfo(self._current_document_id)

            # get the file path
            item_info['path'] = File
            item_info['id'] = str(os.path.basename(File))

            # update item _id and title
            self.splitView.updateItem(
                self._current_document_id,
                item_info['id']
            )
            self._current_document_id = item_info['id']

            # write contents to file
            with open(File, 'w') as f:
                content = str(item_info['doc'].toPlainText())
                f.write(content)

            self.logger.info(f'{File} saved')

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

    def dragEnterEvent(self, event):
        """
        filters drag events to facilitate
        drag and drop functionality

        args: event
            QEvent created by the PySide2 API
        """

        # check if item being dragged in has a path or not
        self.logger.debug('dragEnterEvent detected')
        if event.mimeData().hasUrls():
            event.accept()  # if has path, allow drops

    def dropEvent(self, event):
        """
        filters drop events to facilitate
        drag and drop functionality

        args: event
            QEvent created by the PySide2 API
        """

        # if okayed by the dragEnterEvent
        self.logger.debug('dropEvent detected')
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            if os.path.isfile(path):
                self.open(path)

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

    def load_workbench(self, index):
        """
        loads in a workbench when called by the the deviceComboBox's
        currentItemChanged signal
        also handles cleanup when when workbench is deselcted

        args:
            index: positional argument emited by the device_comboBox
        """

        # close workbench
        if index == 0:
            # close wb_toolbar
            self.wb_toolbar.clear()
            self.wb_toolbar.hide()
            if self.wb_widget is not None:
                # delete widget from memory
                self.wb_widget.deleteLater()
            # clean up parents references to workbench
            self.wb_widget = None
            self.wb = None

        # open workbench
        else:
            # dynamically import wb based on device selection
            # this is the reason that the naming convention is important
            self.logger.info('loading workbench...')
            self.wb_toolbar.clear()

            # garbage cleanup if necessary
            if self.wb_widget is not None:
                old = self.wb_widget
                old.deleteLater()

            # get the new workbench contents
            self.wb_widget = QtWidgets.QWidget()
            device = self.device_comboBox.currentText()
            class_name = ''.join(['my_', device, '_wb'])
            module_path = ''.join(['wb.', device, '.', class_name])
            self.dynamic_import(module_path, class_name)
            wb = getattr(self._module, class_name)()
            self.wb = wb.run_integrated(parent=self)

            # put contents in toolbar
            self.wb_toolbar.addWidget(self.wb_widget)
            self.parent.addToolBarBreak()  # add new row on toolbar
            self.parent.addToolBar(self.wb_toolbar)
            self.wb_toolbar.show()
            self.logger.info('workbench loaded')

    def dynamic_import(self, module_path, module_name):
        """
        takes a module path and module name and dynamically
        imports it, and assigns self._module.

        if not assigned to self._module, the import is
        cleaned up at the end of the function.
        """

        self.logger.debug('importing workbench module')
        self._module = __import__(module_path, fromlist=[module_name])

    # -----------------------------------------------------------------------
    #                       __  __   _
    #                      |  \/  | (_)
    #                      | \  / |  _   ___    ___
    #                      | |\/| | | | / __|  / __|
    #                      | |  | | | | \__ \ | (__
    #                      |_|  |_| |_| |___/  \___|
    # -----------------------------------------------------------------------

    def set_statusbar_right_text(self, text):
        """
        sets the text for the right side
        of the status bar
        """

        self.stat_label.setText(f'current: {text}')

    def find(self):
        """
        find function for splitViewTabWidget text,
        called when the find_pushButton clicked signal emitted
        """

        text = self.find_lineEdit.text()  # string to find
        self.logger.debug(f'searching text for {text}')
        item = self.get_current_plainTextEdit()
        item.setFocus()  # ensures the text gets highlighted
        item.find(text)  # attempts to find the next instance

    def replace(self):
        """
        replace function for splitViewTabWidget text
        called when the replace_pushButton clicked signal emitted
        """

        new = self.replace_lineEdit.text()  # get new text
        self.logger.debug(f'replacement text is {new}')
        item = self.get_current_plainTextEdit()
        item.textCursor().removeSelectedText()  # remove old
        item.textCursor().insertText(new)  # insert new

    @property
    def doc_count(self):
        """
        indexes the document count automatically
        when the doc_count property is used
        """

        self.d_count += 1
        return self.d_count

    @property
    def parent(self):
        """
        returns the most up to date parent
        when the parent attribute is used
        """

        return self.centralwidget.parentWidget()
