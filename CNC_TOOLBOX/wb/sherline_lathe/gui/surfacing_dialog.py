# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Samuel\Documents\CodingProjects\Python\in_progress\CNC_TOOLBOX\wb\sherline_lathe\gui\surfacing_dialog.ui',
# licensing of 'c:\Users\Samuel\Documents\CodingProjects\Python\in_progress\CNC_TOOLBOX\wb\sherline_lathe\gui\surfacing_dialog.ui' applies.
#
# Created: Mon Jan 27 19:34:42 2020
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_surfacing_Dialog(object):
    def setupUi(self, surfacing_Dialog):
        surfacing_Dialog.setObjectName("surfacing_Dialog")
        surfacing_Dialog.resize(288, 324)
        self.gridLayout = QtWidgets.QGridLayout(surfacing_Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.depth_label = QtWidgets.QLabel(surfacing_Dialog)
        self.depth_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.depth_label.setObjectName("depth_label")
        self.gridLayout.addWidget(self.depth_label, 0, 0, 1, 1)
        self.depth_lineEdit = QtWidgets.QLineEdit(surfacing_Dialog)
        self.depth_lineEdit.setObjectName("depth_lineEdit")
        self.gridLayout.addWidget(self.depth_lineEdit, 0, 1, 1, 1)
        self.length_label = QtWidgets.QLabel(surfacing_Dialog)
        self.length_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.length_label.setObjectName("length_label")
        self.gridLayout.addWidget(self.length_label, 1, 0, 1, 1)
        self.length_lineEdit = QtWidgets.QLineEdit(surfacing_Dialog)
        self.length_lineEdit.setObjectName("length_lineEdit")
        self.gridLayout.addWidget(self.length_lineEdit, 1, 1, 1, 1)
        self.feed_label = QtWidgets.QLabel(surfacing_Dialog)
        self.feed_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.feed_label.setObjectName("feed_label")
        self.gridLayout.addWidget(self.feed_label, 2, 0, 1, 1)
        self.feed_lineEdit = QtWidgets.QLineEdit(surfacing_Dialog)
        self.feed_lineEdit.setObjectName("feed_lineEdit")
        self.gridLayout.addWidget(self.feed_lineEdit, 2, 1, 1, 1)
        self.rpm_label = QtWidgets.QLabel(surfacing_Dialog)
        self.rpm_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.rpm_label.setObjectName("rpm_label")
        self.gridLayout.addWidget(self.rpm_label, 3, 0, 1, 1)
        self.rpm_lineEdit = QtWidgets.QLineEdit(surfacing_Dialog)
        self.rpm_lineEdit.setObjectName("rpm_lineEdit")
        self.gridLayout.addWidget(self.rpm_lineEdit, 3, 1, 1, 1)
        self.unit_label = QtWidgets.QLabel(surfacing_Dialog)
        self.unit_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.unit_label.setObjectName("unit_label")
        self.gridLayout.addWidget(self.unit_label, 4, 0, 1, 1)
        self.unit_comboBox = QtWidgets.QComboBox(surfacing_Dialog)
        self.unit_comboBox.setObjectName("unit_comboBox")
        self.gridLayout.addWidget(self.unit_comboBox, 4, 1, 1, 1)
        self.create_pushButton = QtWidgets.QPushButton(surfacing_Dialog)
        self.create_pushButton.setObjectName("create_pushButton")
        self.gridLayout.addWidget(self.create_pushButton, 5, 1, 1, 1)

        self.retranslateUi(surfacing_Dialog)
        QtCore.QMetaObject.connectSlotsByName(surfacing_Dialog)

    def retranslateUi(self, surfacing_Dialog):
        surfacing_Dialog.setWindowTitle(QtWidgets.QApplication.translate("surfacing_Dialog", "Surfacing_Dialog", None, -1))
        self.depth_label.setText(QtWidgets.QApplication.translate("surfacing_Dialog", "depth", None, -1))
        self.length_label.setText(QtWidgets.QApplication.translate("surfacing_Dialog", "length", None, -1))
        self.feed_label.setText(QtWidgets.QApplication.translate("surfacing_Dialog", "feed rate\n"
"[units/min]", None, -1))
        self.rpm_label.setText(QtWidgets.QApplication.translate("surfacing_Dialog", "rpm", None, -1))
        self.unit_label.setText(QtWidgets.QApplication.translate("surfacing_Dialog", "units", None, -1))
        self.create_pushButton.setText(QtWidgets.QApplication.translate("surfacing_Dialog", "create gcode", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    surfacing_Dialog = QtWidgets.QDialog()
    ui = Ui_surfacing_Dialog()
    ui.setupUi(surfacing_Dialog)
    surfacing_Dialog.show()
    sys.exit(app.exec_())

