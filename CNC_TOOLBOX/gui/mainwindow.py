# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(755, 652)
        MainWindow.setDocumentMode(True)
        self.actionopen = QAction(MainWindow)
        self.actionopen.setObjectName(u"actionopen")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.cw_gridLayout = QGridLayout(self.centralwidget)
        self.cw_gridLayout.setObjectName(u"cw_gridLayout")
        self.cw_gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.placeHolder = QWidget(self.centralwidget)
        self.placeHolder.setObjectName(u"placeHolder")

        self.cw_gridLayout.addWidget(self.placeHolder, 1, 0, 1, 2)

        self.toolbar_widget = QWidget(self.centralwidget)
        self.toolbar_widget.setObjectName(u"toolbar_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolbar_widget.sizePolicy().hasHeightForWidth())
        self.toolbar_widget.setSizePolicy(sizePolicy)
        self.toolbar_widget.setMinimumSize(QSize(0, 0))
        self.gridLayout_6 = QGridLayout(self.toolbar_widget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.device_comboBox = QComboBox(self.toolbar_widget)
        self.device_comboBox.setObjectName(u"device_comboBox")
        self.device_comboBox.setMinimumSize(QSize(150, 0))

        self.gridLayout_6.addWidget(self.device_comboBox, 0, 1, 1, 1)

        self.copy_radio = QRadioButton(self.toolbar_widget)
        self.copy_radio.setObjectName(u"copy_radio")
        self.copy_radio.setCheckable(True)
        self.copy_radio.setChecked(True)
        self.copy_radio.setAutoExclusive(True)

        self.gridLayout_6.addWidget(self.copy_radio, 0, 4, 1, 1)

        self.overwrite_radio = QRadioButton(self.toolbar_widget)
        self.overwrite_radio.setObjectName(u"overwrite_radio")

        self.gridLayout_6.addWidget(self.overwrite_radio, 0, 3, 1, 1)

        self.device_label = QLabel(self.toolbar_widget)
        self.device_label.setObjectName(u"device_label")
        self.device_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_6.addWidget(self.device_label, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 2, 1, 1)


        self.cw_gridLayout.addWidget(self.toolbar_widget, 0, 0, 1, 2)

        self.findReplaceWidget = QWidget(self.centralwidget)
        self.findReplaceWidget.setObjectName(u"findReplaceWidget")
        self.gridLayout = QGridLayout(self.findReplaceWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_3 = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)

        self.find_pushButton = QPushButton(self.findReplaceWidget)
        self.find_pushButton.setObjectName(u"find_pushButton")

        self.gridLayout.addWidget(self.find_pushButton, 2, 3, 1, 1)

        self.find_lineEdit = QLineEdit(self.findReplaceWidget)
        self.find_lineEdit.setObjectName(u"find_lineEdit")

        self.gridLayout.addWidget(self.find_lineEdit, 2, 1, 1, 1)

        self.replace_pushButton = QPushButton(self.findReplaceWidget)
        self.replace_pushButton.setObjectName(u"replace_pushButton")

        self.gridLayout.addWidget(self.replace_pushButton, 2, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 6, 1, 1)

        self.replace_lineEdit = QLineEdit(self.findReplaceWidget)
        self.replace_lineEdit.setObjectName(u"replace_lineEdit")

        self.gridLayout.addWidget(self.replace_lineEdit, 2, 2, 1, 1)

        self.hideButton = QToolButton(self.findReplaceWidget)
        self.hideButton.setObjectName(u"hideButton")
        self.hideButton.setIconSize(QSize(16, 16))
        self.hideButton.setToolButtonStyle(Qt.ToolButtonTextOnly)

        self.gridLayout.addWidget(self.hideButton, 2, 5, 1, 1)


        self.cw_gridLayout.addWidget(self.findReplaceWidget, 2, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 755, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.bottomToolBar = QToolBar(MainWindow)
        self.bottomToolBar.setObjectName(u"bottomToolBar")
        self.bottomToolBar.setMovable(False)
        self.bottomToolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.bottomToolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.BottomToolBarArea, self.bottomToolBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionopen.setText(QCoreApplication.translate("MainWindow", u"open", None))
        self.copy_radio.setText(QCoreApplication.translate("MainWindow", u"copy", None))
        self.overwrite_radio.setText(QCoreApplication.translate("MainWindow", u"overwrite", None))
        self.device_label.setText(QCoreApplication.translate("MainWindow", u"device", None))
        self.find_pushButton.setText(QCoreApplication.translate("MainWindow", u"Find", None))
        self.find_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Find", None))
        self.replace_pushButton.setText(QCoreApplication.translate("MainWindow", u"Replace", None))
        self.replace_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Replace", None))
        self.hideButton.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.bottomToolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"findReplaceWidget", None))
    # retranslateUi

