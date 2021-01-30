import unittest

from pathlib import Path
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
        files, folders = fb.list_dir(fb.curdir)
        self.assertTrue(len(files))
        self.assertTrue(len(folders))
        # run a failing case
        with self.assertRaises(ValueError):
            fb.list_dir(str(__file__))

    def test_up_one(self):
        # part that works
        fb = FileBrowser()
        fb.up_one()
        with self.assertRaises(ValueError):
            while fb.up_one():
                pass


if __name__ == "__main__":
    unittest.main()