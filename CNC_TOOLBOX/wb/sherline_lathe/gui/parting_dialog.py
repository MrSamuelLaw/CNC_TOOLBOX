# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Samuel\Documents\CodingProjects\Python\in_progress\CNC_TOOLBOX\wb\sherline_lathe\gui\parting_dialog.ui',
# licensing of 'c:\Users\Samuel\Documents\CodingProjects\Python\in_progress\CNC_TOOLBOX\wb\sherline_lathe\gui\parting_dialog.ui' applies.
#
# Created: Mon Jan 27 19:34:41 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_parting_dialog(object):
    def setupUi(self, parting_dialog):
        parting_dialog.setObjectName("parting_dialog")
        parting_dialog.resize(301, 300)
        self.gridLayout = QtWidgets.QGridLayout(parting_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.feed_label = QtWidgets.QLabel(parting_dialog)
        self.feed_label.setObjectName("feed_label")
        self.gridLayout.addWidget(self.feed_label, 0, 0, 1, 1)
        self.speed_lineEdit = QtWidgets.QLineEdit(parting_dialog)
        self.speed_lineEdit.setObjectName("speed_lineEdit")
        self.gridLayout.addWidget(self.speed_lineEdit, 1, 1, 1, 1)
        self.feed_lineEdit = QtWidgets.QLineEdit(parting_dialog)
        self.feed_lineEdit.setObjectName("feed_lineEdit")
        self.gridLayout.addWidget(self.feed_lineEdit, 0, 1, 1, 1)
        self.speed_label = QtWidgets.QLabel(parting_dialog)
        self.speed_label.setObjectName("speed_label")
        self.gridLayout.addWidget(self.speed_label, 1, 0, 1, 1)
        self.diameter_label = QtWidgets.QLabel(parting_dialog)
        self.diameter_label.setObjectName("diameter_label")
        self.gridLayout.addWidget(self.diameter_label, 2, 0, 1, 1)
        self.diameter_lineEdit = QtWidgets.QLineEdit(parting_dialog)
        self.diameter_lineEdit.setObjectName("diameter_lineEdit")
        self.gridLayout.addWidget(self.diameter_lineEdit, 2, 1, 1, 1)
        self.unit_label = QtWidgets.QLabel(parting_dialog)
        self.unit_label.setObjectName("unit_label")
        self.gridLayout.addWidget(self.unit_label, 3, 0, 1, 1)
        self.unit_comboBox = QtWidgets.QComboBox(parting_dialog)
        self.unit_comboBox.setObjectName("unit_comboBox")
        self.gridLayout.addWidget(self.unit_comboBox, 3, 1, 1, 1)
        self.generate_button = QtWidgets.QPushButton(parting_dialog)
        self.generate_button.setObjectName("generate_button")
        self.gridLayout.addWidget(self.generate_button, 4, 1, 1, 1)

        self.retranslateUi(parting_dialog)
        QtCore.QMetaObject.connectSlotsByName(parting_dialog)
        parting_dialog.setTabOrder(self.feed_lineEdit, self.speed_lineEdit)
        parting_dialog.setTabOrder(self.speed_lineEdit, self.diameter_lineEdit)
        parting_dialog.setTabOrder(self.diameter_lineEdit, self.unit_comboBox)
        parting_dialog.setTabOrder(self.unit_comboBox, self.generate_button)

    def retranslateUi(self, parting_dialog):
        parting_dialog.setWindowTitle(QtWidgets.QApplication.translate("parting_dialog", "Parting Dialog", None, -1))
        self.feed_label.setText(QtWidgets.QApplication.translate("parting_dialog", "feedrate\n"
"[units/min]", None, -1))
        self.speed_label.setText(QtWidgets.QApplication.translate("parting_dialog", "surface speed\n"
"[units/min]", None, -1))
        self.diameter_label.setText(QtWidgets.QApplication.translate("parting_dialog", "diameter", None, -1))
        self.unit_label.setText(QtWidgets.QApplication.translate("parting_dialog", "units", None, -1))
        self.generate_button.setText(QtWidgets.QApplication.translate("parting_dialog", "generate gcode", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    parting_dialog = QtWidgets.QDialog()
    ui = Ui_parting_dialog()
    ui.setupUi(parting_dialog)
    parting_dialog.show()
    sys.exit(app.exec_())

