# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Samuel\Documents\CodingProjects\Python\in_progress\CNC_TOOL_BOX\CNC_TOOLBOX_DEV\wb\sherline_lathe\gui\sherline_lathe_wb.ui',
# licensing of 'C:\Users\Samuel\Documents\CodingProjects\Python\in_progress\CNC_TOOL_BOX\CNC_TOOLBOX_DEV\wb\sherline_lathe\gui\sherline_lathe_wb.ui' applies.
#
# Created: Tue Dec 24 10:32:14 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_sherline_lathe_workbench(object):
    def setupUi(self, sherline_lathe_workbench):
        sherline_lathe_workbench.setObjectName("sherline_lathe_workbench")
        sherline_lathe_workbench.resize(747, 94)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(sherline_lathe_workbench.sizePolicy().hasHeightForWidth())
        sherline_lathe_workbench.setSizePolicy(sizePolicy)
        sherline_lathe_workbench.setFrameShape(QtWidgets.QFrame.Box)
        sherline_lathe_workbench.setFrameShadow(QtWidgets.QFrame.Sunken)
        sherline_lathe_workbench.setLineWidth(1)
        self.gridLayout_2 = QtWidgets.QGridLayout(sherline_lathe_workbench)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(sherline_lathe_workbench)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.in_radiobutton = QtWidgets.QRadioButton(self.widget)
        self.in_radiobutton.setChecked(True)
        self.in_radiobutton.setObjectName("in_radiobutton")
        self.gridLayout.addWidget(self.in_radiobutton, 0, 0, 1, 1)
        self.mm_radiobutton = QtWidgets.QRadioButton(self.widget)
        self.mm_radiobutton.setObjectName("mm_radiobutton")
        self.gridLayout.addWidget(self.mm_radiobutton, 0, 1, 1, 1)
        self.number_checkbox = QtWidgets.QCheckBox(self.widget)
        self.number_checkbox.setChecked(True)
        self.number_checkbox.setObjectName("number_checkbox")
        self.gridLayout.addWidget(self.number_checkbox, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.widget, 0, 6, 1, 1)
        self.surfacing_pushButton = QtWidgets.QPushButton(sherline_lathe_workbench)
        self.surfacing_pushButton.setObjectName("surfacing_pushButton")
        self.gridLayout_2.addWidget(self.surfacing_pushButton, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(sherline_lathe_workbench)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 3, 1, 1)
        self.format_button = QtWidgets.QPushButton(sherline_lathe_workbench)
        self.format_button.setMaximumSize(QtCore.QSize(125, 16777215))
        self.format_button.setObjectName("format_button")
        self.gridLayout_2.addWidget(self.format_button, 0, 7, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.offset_field = QtWidgets.QLineEdit(sherline_lathe_workbench)
        self.offset_field.setMaximumSize(QtCore.QSize(75, 16777215))
        self.offset_field.setPlaceholderText("")
        self.offset_field.setObjectName("offset_field")
        self.gridLayout_2.addWidget(self.offset_field, 0, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(sherline_lathe_workbench)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 5, 1, 1)
        self.parting_pushButton = QtWidgets.QPushButton(sherline_lathe_workbench)
        self.parting_pushButton.setObjectName("parting_pushButton")
        self.gridLayout_2.addWidget(self.parting_pushButton, 0, 1, 1, 1)

        self.retranslateUi(sherline_lathe_workbench)
        QtCore.QMetaObject.connectSlotsByName(sherline_lathe_workbench)

    def retranslateUi(self, sherline_lathe_workbench):
        sherline_lathe_workbench.setWindowTitle(QtWidgets.QApplication.translate("sherline_lathe_workbench", "Frame", None, -1))
        self.in_radiobutton.setText(QtWidgets.QApplication.translate("sherline_lathe_workbench", "in", None, -1))
        self.mm_radiobutton.setText(QtWidgets.QApplication.translate("sherline_lathe_workbench", "mm", None, -1))
        self.number_checkbox.setText(QtWidgets.QApplication.translate("sherline_lathe_workbench", "numbered\n"
"    lines", None, -1))
        self.surfacing_pushButton.setText(QtWidgets.QApplication.translate("sherline_lathe_workbench", "surfacing", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("sherline_lathe_workbench", "offset\n"
"(defaults to G54)", None, -1))
        self.format_button.setText(QtWidgets.QApplication.translate("sherline_lathe_workbench", "format", None, -1))
        self.offset_field.setText(QtWidgets.QApplication.translate("sherline_lathe_workbench", "G54", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("sherline_lathe_workbench", "units", None, -1))
        self.parting_pushButton.setText(QtWidgets.QApplication.translate("sherline_lathe_workbench", "parting", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    sherline_lathe_workbench = QtWidgets.QFrame()
    ui = Ui_sherline_lathe_workbench()
    ui.setupUi(sherline_lathe_workbench)
    sherline_lathe_workbench.show()
    sys.exit(app.exec_())

