import unittest
from unittest.case import TestCase
from modules.filebrowser import FileBrowser


class TestFileBrowser(unittest.TestCase):

    def test_current_directory(self):
        fb1 = FileBrowser()
        fb2 = FileBrowser()
        fb1.curdir = fb1.curdir.parent
        fb3 = FileBrowser()
        self.assertNotEqual(str(fb1.curdir), str(fb2.curdir))
        self.assertEqual(str(fb1.curdir), str(fb3.curdir))

    def test_list_dir(self):
        fb = FileBrowser()
        # run a passing case
        items = fb.dir(fb.curdir)
        self.assertTrue(items)
        # run a failing case
        with self.assertRaises(ValueError):
            fb.dir(str(__file__))


if __name__ == "__main__":
    unittest.main()