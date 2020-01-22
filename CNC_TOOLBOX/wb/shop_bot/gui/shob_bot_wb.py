# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Samuel\Documents\CodingProjects\Python\in_progress\CNC_TOOLBOX_DEV\CNC_TOOLBOX_DEV\wb\shop_bot\gui\shob_bot_wb.ui',
# licensing of 'c:\Users\Samuel\Documents\CodingProjects\Python\in_progress\CNC_TOOLBOX_DEV\CNC_TOOLBOX_DEV\wb\shop_bot\gui\shob_bot_wb.ui' applies.
#
# Created: Fri Jan 17 12:28:31 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_shop_bot_wb(object):
    def setupUi(self, shop_bot_wb):
        shop_bot_wb.setObjectName("shop_bot_wb")
        shop_bot_wb.resize(431, 98)
        shop_bot_wb.setFrameShape(QtWidgets.QFrame.Box)
        self.gridLayout = QtWidgets.QGridLayout(shop_bot_wb)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.rect_macro_button = QtWidgets.QPushButton(shop_bot_wb)
        self.rect_macro_button.setObjectName("rect_macro_button")
        self.gridLayout.addWidget(self.rect_macro_button, 0, 2, 1, 1)

        self.retranslateUi(shop_bot_wb)
        QtCore.QMetaObject.connectSlotsByName(shop_bot_wb)

    def retranslateUi(self, shop_bot_wb):
        shop_bot_wb.setWindowTitle(QtWidgets.QApplication.translate("shop_bot_wb", "Frame", None, -1))
        self.rect_macro_button.setText(QtWidgets.QApplication.translate("shop_bot_wb", "rect_macro", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    shop_bot_wb = QtWidgets.QFrame()
    ui = Ui_shop_bot_wb()
    ui.setupUi(shop_bot_wb)
    shop_bot_wb.show()
    sys.exit(app.exec_())

