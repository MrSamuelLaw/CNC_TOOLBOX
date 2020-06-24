#!/usr/bin/env python3

import unittest
from gparse.rs_274_parser import rs274Parser
from rs_274_plotter import rs274Plotter


class test_rs274Plotter(unittest.TestCase):

    def setUp(self):
        self.parser = rs274Parser()
        self.plotter = rs274Plotter()

    def test_load_gcode(self):
        gcode = "G00 X-0.50 Y0.0 z5.0 (comment)\n\n"
        gcode = self.parser.parse_gcode(gcode)
        self.plotter.load_gcode(gcode)


