#!/usr/bin/env python


from sys import path
path.append('../')
from sherline_lathe.sw_2_linuxCNC_formatter import sw_2_linuxCNC_formatter
import unittest


class test_sw_2_linuxCNC_formatter(unittest.TestCase):

    def test_format(self):
        my_l = sw_2_linuxCNC_formatter()
        File = ("test\\nc_test_files\\"
                "nc_no_edits.nc")
        with open(File, 'r') as f:
            File = f.read()
        first_run = my_l.format(File, 'IN', 'G54')
        # print('----------First Run --------------')
        # print(first_run)
        second_run = my_l.format(first_run, 'IN', 'G54')
        # print('----------Second Run --------------')
        # print(second_run)
        # self.assertEqual(first_run, second_run)

    def test_set_units(self):
        my_l = sw_2_linuxCNC_formatter()
        result = my_l.set_units("m")
        self.assertEqual(result, -1)
        result = my_l.set_units("MM")
        self.assertEqual(result, None)
        result = my_l.set_units("IN")
        self.assertEqual(result, None)

    def test_set_offset(self):
        my_l = sw_2_linuxCNC_formatter()
        result = my_l.set_offset("G80")
        self.assertEqual(result, -1)
        result = my_l.set_offset("G55")
        self.assertEqual(result, None)

    def test_insert_safety_line(self):
        my_l = sw_2_linuxCNC_formatter()
        my_l.set_units("IN")
        my_l.set_offset("G54")
        File = ("test\\nc_test_files\\"
                "nc_no_edits.nc")
        with open(File, 'r') as f:
            File = f.read()
        my_l.load_contents(File)
        result = my_l.insert_safety_line()
        self.assertEqual(result, None)

    def test_delete_B_commands(self):
        my_l = sw_2_linuxCNC_formatter()
        File = ("test\\nc_test_files\\"
                "nc_no_edits.nc")
        with open(File, 'r') as f:
            File = f.read()
        my_l.load_contents(File)
        my_l.delete_B_commands()
        for x in my_l._file_contents:
            if 'B' in x[0] and x[1] == 'code':
                self.assertTrue(False)

    def test_fix_eof(self):
        my_l = sw_2_linuxCNC_formatter()
        File = ("test\\nc_test_files\\"
                "nc_no_edits.nc")
        with open(File, 'r') as f:
            File = f.read()
        my_l.load_contents(File)
        my_l.fix_eof()
        res = my_l._file_contents[-1][0]
        self.assertEqual(res, '%')

    def test_renumber_lines(self):
        my_l = sw_2_linuxCNC_formatter()
        my_l = sw_2_linuxCNC_formatter()
        File = ("test\\nc_test_files\\"
                "nc_no_edits.nc")
        with open(File, 'r') as f:
            File = f.read()
        my_l.load_contents(File)
        my_l.renumber_lines()
        res = my_l._file_contents[0]
        self.assertTrue(res[0], 'N1')

    def test_fix_spindle_cmds(self):
        my_l = sw_2_linuxCNC_formatter()
        File = ("test\\nc_test_files\\"
                "nc_no_edits.nc")
        with open(File, 'r') as f:
            File = f.read()
        my_l.load_contents(File)
        my_l.delete_B_commands()
        my_l.set_offset('G54')
        my_l.set_units('IN')
        my_l.insert_safety_line()
        my_l.fix_eof()
        res = my_l.fix_spindle_cmds()
        self.assertEqual(res, None)

    def test_fix_T_cmds(self):
        my_l = sw_2_linuxCNC_formatter()
        File = ("test\\nc_test_files\\"
                "nc_no_edits.nc")
        with open(File, 'r') as f:
            File = f.read()
        my_l.load_contents(File)
        my_l.set_offset('G54')
        my_l.set_units('IN')
        my_l.insert_safety_line()
        res = my_l.fix_T_commands()
        self.assertEqual(res, None)

    def test_make_tool_table(self):
        my_l = sw_2_linuxCNC_formatter()
        File = ("test\\nc_test_files\\"
                "nc_no_edits.nc")
        with open(File, 'r') as f:
            File = f.read()
        my_l.load_contents(File)
        my_l.set_offset('G54')
        my_l.set_units('IN')
        my_l.insert_safety_line()
        res = my_l.make_tool_tbl()[0][0]
        self.assertEqual(res, 'T101')


if __name__ == "__main__":
    unittest.main()
