#!/usr/bin/env python3


from PySide2 import QtWidgets, QtCore, QtGui
import logging


class splitViewTabWidget_signals(QtCore.QObject):
    """
    custom signals for the splitViewTabWidget
    """

    focusChanged = QtCore.Signal(str)


class splitViewTabWidget(QtWidgets.QWidget):
    """
    splitViewTabWidget consists of two tabWidgets in a split view
    also includes functions that make document management and drag
    and drop easy to implement

    self.twd[<side>] gives access to the tabWidgets

    self.tabDict keeps track of a tabs _id and count

    tab._type, property that is used to allow tabs to
    duplicate properly and is accessed on drop events
    """

    def __init__(self, parent=None):
        super(splitViewTabWidget, self).__init__(parent)
        self._logger = logging.getLogger('log')
        self.signals = splitViewTabWidget_signals()

        # tabWidgets
        self.twd = {'left': QtWidgets.QTabWidget(self), 'right': QtWidgets.QTabWidget(self)}
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

        # set filter functions
        self._filterDict = {
            self.twd['left'].tabBar(): self._tabBarEventFilter,
            self.twd['right'].tabBar(): self._tabBarEventFilter
        }

        # typeDict
        self.typeDict = {
            'text': self.openTextDocument
        }

        # tabDict
        self.tabDict = {}

        # apply layout to self
        self.setLayout(self.layout)
        self.layout.addWidget(self.VSplit)

    def openTextDocument(self, title, text='', side='left', filepath=None):
        # if files are already open somewhere
        self._logger.debug('opening document')
        _id = title
        _id_flag = False
        for key in self.twd.keys():  # iterate through the side
            for i in range(self.twd[key].count()):  # iterate through tabs
                if self.twd[key].widget(i)._id == _id:  # check ids
                    if key == side:  # is document already open on this side?
                        self._logger.debug('failed, document alread open on this side')
                        return  # if so break early
                    else:
                        self._logger.debug('attempting to open on other side')
                        _id_flag = True

        # create new document
        if _id_flag:
            document = self.tabDict[_id]['doc']
            self.tabDict[_id]['count'] += 1
        else:
            document = QtGui.QTextDocument()
            document.setDocumentLayout(QtWidgets.QPlainTextDocumentLayout(document))
            self.tabDict[_id] = {'doc': document, 'count': 1, 'path': filepath}

        # give document to plainTextEdit
        plainTextEdit = QtWidgets.QPlainTextEdit()
        plainTextEdit.setDocument(self.tabDict[_id]['doc'])
        plainTextEdit.insertPlainText(text)
        # assign _id
        plainTextEdit._id = _id
        plainTextEdit._type = 'text'
        # assign addtional functionality
        plainTextEdit.clearText = self.clearText
        plainTextEdit.setAcceptDrops(False)
        # add to tabWidget
        self.twd[side].addTab(plainTextEdit, title)
        self._installTabFilter()
        self._logger.debug('successfully opened document')

    def closeTab(self, index=None):
        self._logger.debug('closing tab')
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
                # if it was also the last one on the right side
                if (side == 'right') and (self.twd['right'].count() == 1):
                    self.twd['right'].hide()

    def getItemInfo(self, _id):
        return self.tabDict[_id]

    def updateItem(self, old_id, new_id):
        for tabWidget in self.twd.values():
            for i in range(tabWidget.count()):
                widget = tabWidget.widget(i)
                if widget._id == old_id:
                    widget._id = new_id
                    tabWidget.setTabText(i, new_id)
        self.tabDict[new_id] = self.tabDict[old_id]
        del self.tabDict[old_id]

    def _tabClicked(self, index):
        # determin sender
        for side in self.twd.keys():
            if bool(self.twd[side].sender()):
                self._clickedTab = self.twd[side].widget(index)
                self._clickedTabText = self.twd[side].tabText(index)

    def _eventFilter(self, Object, event):
        self._filterDict[Object](Object, event)
        return False

    def _tabBarEventFilter(self, Object, event):
        # DRAGGING
        if event.type() == QtCore.QEvent.MouseMove:
            gp = self.mapFromGlobal(event.globalPos())
            p = event.pos()
            if not self.twd['right'].isHidden():
                if (self.twd['left'].geometry().contains(gp)) and (p.y() < self.twd['left'].tabBar().height()):
                    self._canDrop('left')
                    self._normal('right')
                elif (self.twd['right'].geometry().contains(gp)) and (p.y() < self.twd['left'].tabBar().height()):
                    self._canDrop('right')
                    self._normal('left')
                else:
                    self._normal('left')
                    self._normal('right')

            # if right widget is hidden
            else:
                # if it's in the right tenth of the screen
                if (p.x() > self.twd['left'].width()*0.9) and (p.y() > self.twd['left'].tabBar().height()):
                    self.twd['right'].show()
        # DROPPING
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            gp = self.mapFromGlobal(event.globalPos())
            p = event.pos()

            # if not dropped in its own parent
            if not (Object.parent().geometry().contains(gp)):

                # if in the left widget
                if self.twd['left'].geometry().contains(gp):
                    # if on the tabBar
                    if (p.y() < self.twd['left'].tabBar().height()):
                        # prevent duplicates on the same side
                        for i in range(self.twd['left'].count()):
                            if self.twd['left'].widget(i)._id == self._clickedTab._id:
                                self._normal('left')
                                self._normal('right')
                                return
                        self.twd['left'].addTab(self._clickedTab, self._clickedTabText)
                        # close if right one is empty
                        if not self.twd['right'].count():
                            self.twd['right'].hide()
                    else:
                        # get the widget id and
                        _id = self._clickedTab._id
                        _type = self._clickedTab._type
                        # attempt to open it on the otherside
                        self.typeDict[_type](_id)

                # if in the right widget
                elif self.twd['right'].geometry().contains(gp):
                    # if on the tabBar
                    if (p.y() < self.twd['left'].tabBar().height()):
                        # prevent duplicates on the same side
                        for i in range(self.twd['right'].count()):
                            if self.twd['right'].widget(i)._id == self._clickedTab._id:
                                self._normal('left')
                                self._normal('right')
                                return
                        self.twd['right'].addTab(self._clickedTab, self._clickedTabText)
                    else:
                        # get the widget id and
                        _id = self._clickedTab._id
                        _type = self._clickedTab._type
                        # attempt to open it on the otherside
                        self.typeDict[_type](_id, side='right')

            # set all the tabBar stylings back to normal
            self._normal('left')
            self._normal('right')
            if not self.twd['right'].count():
                self.twd['right'].hide()

    def _tabFilter(self, Object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self._currentItem = Object
            self.signals.focusChanged.emit(Object._id)

    def _installTabFilter(self):
        for tabWidget in self.twd.values():
            for i in range(tabWidget.count()):
                tab = tabWidget.widget(i)
                tab.installEventFilter(self)
                self._filterDict[tab] = self._tabFilter

    # TAB BAR STYLING FUNCTIONS

    def _canDrop(self, side):
        self.twd[side].setStyleSheet("""
            QTabBar {
                 background: #727272
            }
        """)

    def _normal(self, side):
        self.twd[side].setStyleSheet('')

    # TEXT ITEM HELPER FUNCTIONS

    def clearText(self):
        """
        clear text while preserving the plainTextEdit's undo stack
        """
        self._logger.info('clearing text')
        # create a instance of a Q cursor with text doc as parent
        curs = QtGui.QTextCursor(self._currentItem.document())
        # select all the content
        curs.select(QtGui.QTextCursor.Document)
        # delete all the content
        curs.deleteChar()
        curs.setPosition(0)


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    app.startingUp()
    # create widget
    window = splitViewTabWidget()
    window.setWindowTitle('splitViewTabWidget')
    window.setMinimumHeight(600)
    window.setMinimumWidth(800)
    # open text in the widget
    window.openTextDocument('title', 'text here', 'left')
    window.openTextDocument('title2', 'different text here', 'right')

    window.show()
    code = app.exec_()
    sys.exit(code)
