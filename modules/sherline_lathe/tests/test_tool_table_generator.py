
import unittest
from pathlib import Path
from modules.sherline_lathe.tool_table_generator import generate


class test_generate_tool_table(unittest.TestCase):

    def test_generate_tool_table(self):
        test_code = ("G20 X0 Y0"
                     "T01 (First Tool)")
        tool_table = generate(test_code)
        self.assertEqual(len(tool_table), 1)

    def test_handle_duplicates(self):
        test_code = ("G20 X0 Y0"
                     "T01 (First Tool)"
                     "T01 (First Tool)")
        tool_table = generate(test_code)
        self.assertEqual(len(tool_table), 1)

    def test_handle_multiple(self):
        test_code = ("G20 X0 Y0"
                     "T01 (First Tool)"
                     "T02 (Second Tool)")
        tool_table = generate(test_code)
        self.assertEqual(len(tool_table), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)