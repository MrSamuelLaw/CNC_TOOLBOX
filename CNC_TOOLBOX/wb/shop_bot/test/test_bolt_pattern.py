#!/usr/bin/env python

from bolt_pattern import bolt_pattern
from wb.shop_bot.gui.rect_gen_dialog import Ui_Dialog
import unittest


class test_bolt_pattern(unittest.TestCase):

    def test_set_units(self):
        bp = bolt_pattern()
        rslt = bp._set_units('mm')
        self.assertEqual(2, rslt)

    def test_set_rect(self):
        bp = bolt_pattern()
        rslt = bp._set_rect(10,10)
        self.assertEqual(4, len(rslt))

    def test_set_depth(self):
        bp = bolt_pattern()
        rslt = bp._set_depth(0.02)
        self.assertEqual(rslt, 0.02)

    def test_get_gcode(self):
        bp = bolt_pattern()
        bp.get_rect_gcode('in', 10, 10, 0.02)