#!/usr/bin/env python


# from lathe_nc_make_ready import lathe_nc_make_ready
from sw_2_linuxCNC_formatter import sw_2_linuxCNC_formatter
import unittest


class test_sw_2_linuxCNC_formatter(unittest.TestCase):

    def test_format(self):
        my_l = sw_2_linuxCNC_formatter()
        my_l._load_file('test\\nc_test_files\\nc_no_edits.nc')
        first_run = my_l.format(my_l._file_contents, 'IN', 'G54')
        second_run = my_l.format(first_run, 'IN', 'G54')
        self.assertEqual(first_run, second_run)

    def test_set_file(self):
        my_l = sw_2_linuxCNC_formatter()
        result = my_l._load_file("non\\existent\\file.txt")
        self.assertEqual(result, -1)

    def test_only_nc_files(self):
        my_l = sw_2_linuxCNC_formatter()
        result = my_l._load_file("test\\nc_test_files\\nc_no_edits.set")
        self.assertEqual(result, -2)

    def test_read_nc_file_to_memory(self):
        my_l = sw_2_linuxCNC_formatter()
        result = my_l._load_file("test\\nc_test_files\\"
                                "nc_no_edits.nc")

        self.assertEqual(result, 1)

    def test_set_units(self):
        my_l = sw_2_linuxCNC_formatter()
        result = my_l._set_units("m")
        self.assertEqual(result, -3)
        result = my_l._set_units("MM")
        self.assertEqual(result, 2)
        result = my_l._set_units("IN")
        self.assertEqual(result, 2)

    def test_set_offset(self):
        my_l = sw_2_linuxCNC_formatter()
        result = my_l._set_offset("G80")
        self.assertEqual(result, -4)
        result = my_l._set_offset("G55")
        self.assertEqual(result, 3)

    def test_insert_safety_line(self):
        my_l = sw_2_linuxCNC_formatter()
        my_l._set_units("IN")
        my_l._set_offset("G54")
        my_l._load_file("test\\nc_test_files\\"
                       "nc_no_edits.nc")
        result = my_l._insert_safety_line()
        self.assertEqual(result, 8)

    def test_delete_B_commands(self):
        my_l = sw_2_linuxCNC_formatter()
        my_l._load_file("test\\nc_test_files\\"
                       "nc_testfile.nc")
        result = my_l._delete_B_commands()
        self.assertEqual(result, 4)

    def test_delete_after_keyword(self):
        my_l = sw_2_linuxCNC_formatter()
        my_l._load_file("test\\nc_test_files\\"
                       "nc_no_edits.nc")
        result = my_l._delete_after_keyword('M30', my_l._file_contents)
        self.assertEqual(result, 5)

    def test_fix_eof(self):
        my_l = sw_2_linuxCNC_formatter()
        my_l._load_file("test\\nc_test_files\\"
                       "nc_no_edits.nc")
        result = my_l._fix_eof()
        self.assertEqual(result, 6)

    def test_renumber_lines(self):
        my_l = sw_2_linuxCNC_formatter()
        my_l._load_file("test\\nc_test_files\\"
                       "nc_no_edits.nc")
        result = my_l._renumber_lines()
        self.assertEqual(result, 7)

    def test_format_message(self):
        my_l = sw_2_linuxCNC_formatter()
        result = my_l._format_message('test')
        expected = '(MSG, test)'
        self.assertEqual(result, expected)

    def test_fix_spindle_cmds(self):
        my_l = sw_2_linuxCNC_formatter()
        my_l._load_file("test\\nc_test_files\\"
                       "nc_no_edits.nc")
        my_l._delete_B_commands()
        my_l._set_offset('G54')
        my_l._set_units('IN')
        my_l._insert_safety_line()
        my_l._fix_eof()
        my_l._fix_spindle_cmds()

    def test_fix_T_cmds(self):
        my_l = sw_2_linuxCNC_formatter()
        my_l._load_file("test\\nc_test_files\\"
                       "nc_no_edits.nc")
        my_l._delete_B_commands()
        my_l._set_offset('G54')
        my_l._set_units('IN')
        my_l._insert_safety_line()
        my_l._fix_eof()
        my_l._fix_spindle_cmds()
        result = my_l._fix_T_commands()
        self.assertEqual(5, result)
