#!/usr/bin/env python3 -v


import unittest
from rs_274_parser import rs274Parser
from cProfile import Profile
from pstats import Stats


class test_rs274(unittest.TestCase):

    def setUp(self):
        self.parser = rs274Parser()

    def load_file(self):
        with open('test/ring.nc', 'r') as infile:
            text = infile.read()
            return text

    def test_add_comment_flag(self):
        expected = ['(', ')', ';']
        result = self.parser._comment_flags.keys()
        for r in result:
            self.assertTrue(r in expected)

    def test_get_flag_count(self):
        self.parser.get_flag_count('(')
        self.parser.get_flag_count(')')
        self.assertEqual(
            0,
            self.parser._comment_flags['(']['count'][0]
        )

    def test_check_flag_counts(self):
        self.parser.check_flag_counts(lnum=1)

    def test_parse_gcode(self):
        with self.assertRaises(ValueError):
            self.parser.parse_gcode('GG54')
        with self.assertRaises(ValueError):
            self.parser.parse_gcode('(bad brackets')
        with self.assertRaises(ValueError):
            self.parser.parse_gcode(']')
        with self.assertRaises(ValueError):
            self.parser._add_comment_flag(['//'], [-1])
        good = "G54\n(comment)\n%\n;"
        res = self.parser.parse_gcode(good)
        res = [x[0] for x in res]
        res = '\n'.join(res)
        self.assertEqual(res, good)

    def test_run_profiling(self):
        profiler = Profile()
        text = self.load_file()
        n = 1
        text = '\n'.join(([text] * n))
        profiler.runcall(
            self.parser.parse_gcode,
            text
        )
        stats = Stats(profiler)
        stats.strip_dirs()
        stats.sort_stats('cumulative')
        print("="*20)
        stats.print_stats()

    def test_to_text(self):
        text = self.load_file()
        code = self.parser.parse_gcode(text)
        parsed = self.parser.to_text(code)
        self.assertEqual(text, parsed)

    def test_insert_line(self):
        text = "G54\nX-0.5\nM30\n%"
        code = self.parser.parse_gcode(text)
        line = 'T60 B90.5'
        code = self.parser.insert_line(code, line, code[-1][2])
        self.assertEqual(code[-1][0], 'B90.5')


if __name__ == '__main__':
    tester = test_rs274()
    tester.setUp()
    tester.run_profiling()
