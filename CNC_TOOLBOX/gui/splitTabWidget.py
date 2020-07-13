#!/usr/bin/env python3

# ==========================================
# Author: Samuel Law
# BUGS: N/A
# ==========================================


from PySide2 import QtWidgets, QtCore, QtGui
from itertools import chain
import logging


class splitViewTabWidget_signals(QtCore.QObject):
    """custom signals for the splitViewTabWidget"""

    focusChanged = QtCore.Signal(str)


class splitViewTabWidget(QtWidgets.QWidget):
    """
    splitViewTabWidget consists of two tabWidgets in a split view
    also includes functions that make document management and drag
    and drop easy to implement.
    One thing coders will noticeis the lack of function calls,
    this is due to the need for speed in dynamic ui.
    Function calls in python are expensive in terms of memory and time
    thus this widget uses as few of them as possible

    self.twd[<side>] gives access to the tabWidgets:
        options for <side> are "left" or "right"
        note: short for tabWidgetDict

    self.tabDict keeps track of a tabs _id and count

    never access self._currentItem directly, use getPlainTextEdit instead
    """

    def __init__(self, parent=None):
        super(splitViewTabWidget, self).__init__(parent)
        self.logger = logging.getLogger('log')
        self.signals = splitViewTabWidget_signals()

        # setup tabwidgets
        self.twd = {
            'left': QtWidgets.QTabWidget(self),
            'right': QtWidgets.QTabWidget(self)
        }
        self.twd['left'].setObjectName('left')
        self.twd['right'].setObjectName('right')
        self.twd['left'].setDocumentMode(True)
        self.twd['right'].setDocumentMode(True)
        self.twd['left'].setMovable(True)
        self.twd['right'].setMovable(True)
        self.twd['left'].setTabsClosable(True)
        self.twd['right'].setTabsClosable(True)

        # splitter
        self.VSplit = QtWidgets.QSplitter(self, QtCore.Qt.Vertical)
        self.VSplit.setHandleWidth(0)
        self.VSplit.addWidget(self.twd['left'])
        self.VSplit.addWidget(self.twd['right'])

        # grid_layout
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setVerticalSpacing(0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # connect signals and slots
        self.twd['left'].tabBarClicked.connect(self._tabClicked)
        self.twd['right'].tabBarClicked.connect(self._tabClicked)
        self.twd['left'].tabCloseRequested.connect(self.closeTab)
        self.twd['right'].tabCloseRequested.connect(self.closeTab)

        # event overrides
        # None

        # event filter installs
        self.eventFilter = self._eventFilter
        self.twd['left'].tabBar().installEventFilter(self)
        self.twd['right'].tabBar().installEventFilter(self)

        # set event filter function calls
        self._filterDict = {
            self.twd['left'].tabBar(): self._tabBarEventFilter,
            self.twd['right'].tabBar(): self._tabBarEventFilter
        }

        # tabDict
        self.tabDict = {}

        # apply layout to self
        self.setLayout(self.layout)
        self.layout.addWidget(self.VSplit)

    def openTextDocument(self, title, text='', side='left', filepath=None):
        """
        Opens a new document on the left hand side. If the document is
        already open, it refreshes the document content

        args:
            title:
                will be used the documents _id
            text:
                text to be inserted into the tab
            side:
                which tabWidget to open the document in
            filepath:
                path to associate with the tab
        """

        self.logger.debug('opening document')
        _id = title

        # check if open at all
        if self.tabDict.get(_id, None):
            # if open on this side, refresh the content
            if self.is_on_side(_id, side):
                plainTextEdit = self.getPlainTextEdit(_id)
                plainTextEdit.clearText()
                plainTextEdit.insertPlainText(text)
                return
        else:
            # if it's not open at all, create a new document
            document = QtGui.QTextDocument()
            document.setDocumentLayout(
                QtWidgets.QPlainTextDocumentLayout(document)
            )
            self.tabDict[_id] = {'doc': document, 'count': 1, 'path': filepath}

        # give document to plainTextEdit
        plainTextEdit = QtWidgets.QPlainTextEdit()
        plainTextEdit.setDocument(self.tabDict[_id]['doc'])
        # insert text if any
        plainTextEdit.insertPlainText(text)
        # move cursor to the top of the docuement
        plainTextEdit.moveCursor(QtGui.QTextCursor.Start)
        plainTextEdit.ensureCursorVisible()
        # assign _id
        plainTextEdit._id = _id
        # assign addtional functionality
        plainTextEdit.clearText = self.clearText
        plainTextEdit.setAcceptDrops(False)
        # install event filters
        plainTextEdit.installEventFilter(self)
        self._filterDict[plainTextEdit] = self._tabFilter
        # add to tabWidget
        self.twd[side].addTab(plainTextEdit, _id)
        # move view to new tab
        self.twd[side].setCurrentWidget(plainTextEdit)
        # set current widget and emit _id
        self._currentItem = plainTextEdit
        self.signals.focusChanged.emit(self._currentItem._id)
        self.logger.debug('successfully opened document')

    def copyTextDocument(self, _id, side, force=False):
        """Handles tab copy requests as they attepmt to
        open on each tabwidget"""

        self.logger.debug("copying document")
        # if open on this side, pass
        if self.is_on_side(_id, side) and (not force):
            return

        # else, open it on the other side
        self.tabDict[_id]['count'] += 1
        # give document to plainTextEdit
        plainTextEdit = QtWidgets.QPlainTextEdit()
        plainTextEdit.setDocument(self.tabDict[_id]['doc'])
        # move cursor to the top of the docuement
        plainTextEdit.moveCursor(QtGui.QTextCursor.Start)
        plainTextEdit.ensureCursorVisible()
        # assign _id
        plainTextEdit._id = _id
        # assign addtional functionality
        plainTextEdit.clearText = self.clearText
        plainTextEdit.setAcceptDrops(False)
        # install event filters
        plainTextEdit.installEventFilter(self)
        self._filterDict[plainTextEdit] = self._tabFilter
        # add to tabWidget
        self.twd[side].addTab(plainTextEdit, _id)
        # move view to new tab
        self.twd[side].setCurrentWidget(plainTextEdit)
        # set current widget and emit _id
        self._currentItem = plainTextEdit
        self.signals.focusChanged.emit(self._currentItem._id)
        self.logger.debug('successfully opened document')

    def closeTab(self, index=None):
        """
        closes a tab, if it is the last of
        a shared document, it performs garbage cleanup.
        can be called when the tabCloseRequested signal is emitted
        """

        self.logger.debug('closing tab')
        # determin sender
        for side in self.twd.keys():
            if bool(self.twd[side].sender()):
                # get widget
                if index is None:
                    widget = self._currentTab
                else:
                    widget = self.twd[side].widget(index)
                widget.deleteLater()
                # index the count
                self.tabDict[widget._id]['count'] -= 1

                # delete the document if it was the last one
                if not self.tabDict[widget._id]['count']:
                    del self.tabDict[widget._id]

                # delete the tab from the _filterDict
                del self._filterDict[widget]

                # if it was the last tab on the right side
                if (side == 'right') and (self.twd['right'].count() == 1):
                    self.signals.focusChanged.emit(
                        # update status label
                        self.twd['left'].currentWidget()._id
                    )
                    self.twd['right'].hide()

                # if it was the last tab on the left side
                if (side == 'left') and (self.twd['left'].count() == 1):
                    self.moveTabsLeft()

    def moveTabsLeft(self):
        """moves tabs from the right widget to the left"""
        for i in range(self.twd['right'].count()):
            # get the widget
            widget = self.twd['right'].widget(i)
            # open it on the left side
            self.copyTextDocument(widget._id, side='left', force=True)
            # delete it
            widget.deleteLater()
        # update focus
        self.signals.focusChanged.emit(
            self.twd['right'].currentWidget()._id
        )
        # hade the widget
        self.twd['right'].hide()

    def is_on_side(self, _id, side):
        """returns true of false if the tab with
        given _id is open on that side"""
        ids = [self.twd[side].widget(i)._id for i in range(self.twd[side].count())]
        return (_id in ids)

    def getItemInfo(self, _id):
        """
        used to get plainTextEdit's underlying
        document and path.

        returns a dict with the following
        properties
        {
            _id: also the tab title
            doc: the underlying document that allows
                 synced text between tabs
            path: the documents file path
            count: how many open tabs have the same documents
        }
        """
        return self.tabDict[_id]

    def getPlainTextEdit(self, _id):
        """
        Takes an _id and returns
        associated plainTextEdit if it exists
        raises ValueError if id is not valid
        Exclusivly called by workbench modules
        """
        # is short for plainTextEdit tab
        tabs = [[t.widget(i) for i in range(t.count())] for t in self.twd.values()]
        tabs = chain(*tabs)
        for plainTextEdit in tabs:  # allow for shortcut
            if plainTextEdit._id == _id:
                return plainTextEdit
        raise ValueError("invalide _id")

        # for tabWidget in self.twd.values():
        #     for i in range(tabWidget.count()):
        #         plainTextEdit = tabWidget.widget(i)
        #         if plainTextEdit._id == _id:
        #             return plainTextEdit
        # raise ValueError("invalid _id")

    def updateItem(self, old_id, new_id):
        """
        takes an id and updates it, used
        for files that have been saved under a new
        name.
        """

        for tabWidget in self.twd.values():
            for i in range(tabWidget.count()):
                widget = tabWidget.widget(i)
                if widget._id == old_id:
                    widget._id = new_id
                    tabWidget.setTabText(i, new_id)
        self.tabDict[new_id] = self.tabDict[old_id]
        del self.tabDict[old_id]
        self.signals.focusChanged.emit(new_id)

    #  ______                          _     ______   _   _   _
    # |  ____|                        | |   |  ____| (_) | | | |
    # | |__    __   __   ___   _ __   | |_  | |__     _  | | | |_    ___   _ __   ___
    # |  __|   \ \ / /  / _ \ | '_ \  | __| |  __|   | | | | | __|  / _ \ | '__| / __|
    # | |____   \ V /  |  __/ | | | | | |_  | |      | | | | | |_  |  __/ | |    \__ \
    # |______|   \_/    \___| |_| |_|  \__| |_|      |_| |_|  \__|  \___| |_|    |___/

    def _tabClicked(self, index):
        """
        called when the tabBarClicked signal is emitted
        so the splitTabWidget can know which document
        should have focus

        args:
            index:
                position of tab clicked
        """

        # determin sender
        for side in self.twd.keys():
            if bool(self.twd[side].sender()):
                self._clickedTab = self.twd[side].widget(index)
                self._clickedTabText = self.twd[side].tabText(index)
                self.signals.focusChanged.emit(self._clickedTab._id)

    def _eventFilter(self, Object, event):
        """
        event handler that uses the Object
        to call the correct function
        from the _functionDict
        """

        try:  # checks for key errors
            self._filterDict[Object](Object, event)
        except KeyError:
            pass
        return False  # necessary to prevent errors in QEvent chain

    def _tabBarEventFilter(self, Object, event):
        """
        handles drag and drop functionality
        for the splitViewTabWidget

        note* do NOT split into seperate functions, that would
        cause additional overhead for what is essentally
        a fancy sorter
        """

        # DRAGGING
        if event.type() == QtCore.QEvent.MouseMove:
            gp = self.mapFromGlobal(event.globalPos())  # global point
            p = event.pos()  # local point
            if not self.twd['right'].isHidden():
                # HIGHLIGHT DROP ZONES
                if ((self.twd['left'].geometry().contains(gp)) and
                        (p.y() < self.twd['left'].tabBar().height())):
                    self._canDropLeft()
                elif ((self.twd['right'].geometry().contains(gp)) and
                        (p.y() < self.twd['left'].tabBar().height())):
                    self._canDropRight()
                else:
                    self._normal()
            # if right tabWidget is hidden
            else:
                # if it's in the right tenth of the screen
                if ((p.x() > self.twd['left'].width()*0.9) and
                        (p.y() > self.twd['left'].tabBar().height())):
                    self.twd['right'].show()

        # DROPPING
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            gp = self.mapFromGlobal(event.globalPos())
            p = event.pos()
            # if not dropped in its own parent
            if not (Object.parent().geometry().contains(gp)):

                # DROPPED IN LEFT WIDGET
                if self.twd['left'].geometry().contains(gp):
                    # if on the tabBar
                    if (p.y() < self.twd['left'].tabBar().height()):
                        # prevent duplicates on the same side
                        for i in range(self.twd['left'].count()):
                            if self.twd['left'].widget(i)._id == self._clickedTab._id:
                                self._normal()
                                return
                        self.twd['left'].addTab(self._clickedTab, self._clickedTabText)
                        # close if right one is empty
                        if not self.twd['right'].count():
                            self.twd['right'].hide()
                    else:
                        # get the widget id and
                        _id = self._clickedTab._id
                        # attempt to open it on the otherside
                        self.copyTextDocument(_id, side='left')

                # DROPPED IN THE RIGHT WIDGET
                elif self.twd['right'].geometry().contains(gp):
                    # if on the tabBar
                    if (p.y() < self.twd['left'].tabBar().height()):
                        # prevent duplicates on the same side
                        for i in range(self.twd['right'].count()):
                            if self.twd['right'].widget(i)._id == self._clickedTab._id:
                                self._normal()
                                return
                        self.twd['right'].addTab(self._clickedTab, self._clickedTabText)
                    else:
                        # get the widget id and
                        _id = self._clickedTab._id
                        # attempt to open it on the otherside
                        self.copyTextDocument(_id, side='right')
                    # if left count is zero, move everything to the left widget
                    if not self.twd['left'].count():
                        while self.twd['right'].count() > 0:
                            tab = self.twd['right'].widget(0)
                            text = self.twd['right'].tabText(0)
                            self.twd['left'].addTab(tab, text)

            # set all the tabBar stylings back to normal
            self._normal()
            if not self.twd['right'].count():
                self.twd['right'].hide()

    def _tabFilter(self, Object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self._currentItem = Object
            self.signals.focusChanged.emit(Object._id)

    # --------------------------------------------------------------------------
    #    _____   _             _
    #   / ____| | |           | |
    #  | (___   | |_    __ _  | |_    ___   ___
    #   \___ \  | __|  / _` | | __|  / _ \ / __|
    #   ____) | | |_  | (_| | | |_  |  __/ \__ \
    #  |_____/   \__|  \__,_|  \__|  \___| |___/
    # ---------------------------------------------------------------------------

    # TABBAR STATES
    def _normal(self):
        """set everything to default colors"""
        self.twd['left'].setStyleSheet('')
        self.twd['right'].setStyleSheet('')

    def _canDropLeft(self):
        """set left drop zone to grey"""

        self.twd['left'].setStyleSheet("""
            QTabBar {
                 background: #727272
            }
        """)
        self.twd['right'].setStyleSheet('')

    def _canDropRight(self):
        """set right dropzone to grey"""

        self.twd['right'].setStyleSheet("""
            QTabBar {
                 background: #727272
            }
        """)
        self.twd['left'].setStyleSheet('')

    # ----------------------------------------------------------------------------------
    #   _______                 _
    #  |__   __|               | |
    #     | |      ___  __  __ | |_
    #     | |     / _ \ \ \/ / | __|
    #     | |    |  __/  >  <  | |_
    #   __|_|_    \___| /_/\_\  \__|                                               _
    #  |  \/  |                                                                   | |
    #  | \  / |   __ _   _ __     __ _    __ _    ___   _ __ ___     ___   _ __   | |_
    #  | |\/| |  / _` | | '_ \   / _` |  / _` |  / _ \ | '_ ` _ \   / _ \ | '_ \  | __|
    #  | |  | | | (_| | | | | | | (_| | | (_| | |  __/ | | | | | | |  __/ | | | | | |_
    #  |_|  |_|  \__,_| |_| |_|  \__,_|  \__, |  \___| |_| |_| |_|  \___| |_| |_|  \__|
    #                                     __/ |
    #                                    |___/
    # ----------------------------------------------------------------------------------

    def clearText(self):
        """
        clear text while preserving the plainTextEdit's undo stack
        """
        self.logger.info('clearing text')
        # create a instance of a Q cursor with text doc as parent
        curs = QtGui.QTextCursor(self._currentItem.document())
        # select all the content
        curs.select(QtGui.QTextCursor.Document)
        # delete all the content
        curs.deleteChar()
        curs.setPosition(0)
