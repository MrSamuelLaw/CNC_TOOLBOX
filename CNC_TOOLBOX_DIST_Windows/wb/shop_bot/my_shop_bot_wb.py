#!/usr/bin/env python


from wb.shop_bot.gui.shob_bot_wb import *
from wb.shop_bot.gui.rect_gen_dialog import Ui_Dialog
from wb.shop_bot.bolt_pattern import bolt_pattern
import pyperclip

class my_shop_bot_wb(Ui_shop_bot_wb):

    def run_integrated(self, parent):
        self.load_parent_elements(parent)
        self.setupUi(self.frame)

        # put functions here
        self.rect_macro_button.clicked.connect(self.rect_generator)

        # return self to keep instance alive
        return self

    def load_parent_elements(self, parent):
        self.text_area = parent.text_area
        self.frame = parent.frame

    def rect_generator(self):
        # set the form up
        bp = bolt_pattern()
        dialog = QtWidgets.QDialog()
        form = Ui_Dialog()
        form.setupUi(dialog)
        units = ['in', 'mm']
        for u in units:
            form.unit_combo_box.addItem(u)

        # add functions
        form.generate_button.clicked.connect(dialog.accept)

        # capture the return
        if dialog.exec_():
            try:
                unit = form.unit_combo_box.currentText()
                x = float(form.w_line_edit.text())
                y = float(form.h_line_edit.text())
                depth = float(form.d_line_edit.text())
                output = bp.get_rect_gcode(unit, x, y, depth)
            except Exception as e:
                output = e
            pyperclip.copy(str(output))


