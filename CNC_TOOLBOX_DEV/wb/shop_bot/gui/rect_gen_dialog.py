# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Samuel\Documents\CodingProjects\Python\in_progress\CNC_TOOLBOX_DEV\CNC_TOOLBOX_DEV\wb\shop_bot\gui\rect_gen_dialog.ui',
# licensing of 'c:\Users\Samuel\Documents\CodingProjects\Python\in_progress\CNC_TOOLBOX_DEV\CNC_TOOLBOX_DEV\wb\shop_bot\gui\rect_gen_dialog.ui' applies.
#
# Created: Fri Jan 17 12:28:30 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(272, 312)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.d_label = QtWidgets.QLabel(Dialog)
        self.d_label.setAlignment(QtCore.Qt.AlignCenter)
        self.d_label.setObjectName("d_label")
        self.gridLayout.addWidget(self.d_label, 2, 0, 1, 1)
        self.w_line_edit = QtWidgets.QLineEdit(Dialog)
        self.w_line_edit.setObjectName("w_line_edit")
        self.gridLayout.addWidget(self.w_line_edit, 0, 1, 1, 1)
        self.h_label = QtWidgets.QLabel(Dialog)
        self.h_label.setAlignment(QtCore.Qt.AlignCenter)
        self.h_label.setObjectName("h_label")
        self.gridLayout.addWidget(self.h_label, 1, 0, 1, 1)
        self.w_label = QtWidgets.QLabel(Dialog)
        self.w_label.setAlignment(QtCore.Qt.AlignCenter)
        self.w_label.setObjectName("w_label")
        self.gridLayout.addWidget(self.w_label, 0, 0, 1, 1)
        self.unit_label = QtWidgets.QLabel(Dialog)
        self.unit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.unit_label.setObjectName("unit_label")
        self.gridLayout.addWidget(self.unit_label, 3, 0, 1, 1)
        self.h_line_edit = QtWidgets.QLineEdit(Dialog)
        self.h_line_edit.setObjectName("h_line_edit")
        self.gridLayout.addWidget(self.h_line_edit, 1, 1, 1, 1)
        self.unit_combo_box = QtWidgets.QComboBox(Dialog)
        self.unit_combo_box.setObjectName("unit_combo_box")
        self.gridLayout.addWidget(self.unit_combo_box, 3, 1, 1, 1)
        self.generate_button = QtWidgets.QPushButton(Dialog)
        self.generate_button.setObjectName("generate_button")
        self.gridLayout.addWidget(self.generate_button, 4, 1, 1, 1)
        self.d_line_edit = QtWidgets.QLineEdit(Dialog)
        self.d_line_edit.setObjectName("d_line_edit")
        self.gridLayout.addWidget(self.d_line_edit, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.w_line_edit, self.h_line_edit)
        Dialog.setTabOrder(self.h_line_edit, self.d_line_edit)
        Dialog.setTabOrder(self.d_line_edit, self.unit_combo_box)
        Dialog.setTabOrder(self.unit_combo_box, self.generate_button)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.d_label.setText(QtWidgets.QApplication.translate("Dialog", "Depth", None, -1))
        self.h_label.setText(QtWidgets.QApplication.translate("Dialog", "Height", None, -1))
        self.w_label.setText(QtWidgets.QApplication.translate("Dialog", "Width", None, -1))
        self.unit_label.setText(QtWidgets.QApplication.translate("Dialog", "Units", None, -1))
        self.generate_button.setText(QtWidgets.QApplication.translate("Dialog", "generate", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

