#!/usr/bin/env python3

import unittest
from gparse.rs_274_parser import rs274Parser
from rs_274_plotter import rs274Plotter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class test_rs274Plotter(unittest.TestCase):

    def setUp(self):
        config_path = "test/parser.config"
        self.plotter = rs274Plotter()
        self.parser = rs274Parser()

    def test_load_gcode(self):
        gcode = "G00 X-0.50 Y0.0 z5.0 (comment)\n\n"
        gcode = self.parser.parse_gcode(gcode)
        self.plotter.load_gcode(gcode)
        with self.assertRaises(AttributeError):
            self.plotter.load_gcode(gcode)

    def test_clear_gcode(self):
        gcode = "G00 X0Y0Z0"
        gcode = self.parser.parse_gcode(gcode)
        self.plotter.load_gcode(gcode)
        self.plotter.clear_gcode()
        self.plotter.load_gcode(gcode)

    def test_group_gcode_by_line(self):
        gcode = """
        G01 F100
        X0Y0Z0
        X1Y1Z1
        """
        lnum = 3
        gcode = self.parser.parse_gcode(gcode)
        self.plotter.load_gcode(gcode)
        lines = self.plotter.group_gcode_by_line(
            self.plotter.gcode
        )
        self.assertEqual(len(lines), lnum)

    def t_run(self):
        gcode = """
        G01 F100
        x0y0z0
        x1y1z1
        x1y0z0
        x0y0z0
        """
        gcode = self.parser.parse_gcode(gcode)
        self.plotter.load_gcode(gcode)
        self.plotter.setup_axis(
            linear={
                "X": "U",
                "Y": "V",
                "Z": "W"
            },
            arc={}
        )
        points = self.plotter.generate_points()
        x, y, z = [], [], []
        for a, b, c in points:
            x.append(a)
            y.append(b)
            z.append(c)

        fig = plt.figure()
        ax = fig.gca(projection="3d")

        ax.plot(x, y, z)
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        ax.set_zlabel("Z axis")
        plt.show()
        input("press enter")
