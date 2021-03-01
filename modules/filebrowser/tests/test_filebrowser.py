import unittest
from datetime import datetime
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

    def test_st_mtime_to_string(self):
        fb = FileBrowser()
        # create a time stamp
        expected = datetime.now()
        # convert to string and back again
        string_time = fb.st_mtime_to_string(expected.timestamp())
        result = datetime.strptime(string_time, fb._timestamp_format)
        # assert the parts we care about are equal
        self.assertEqual(expected.day, result.day)
        self.assertEqual(expected.month, result.month)
        self.assertEqual(expected.year, result.year)
        self.assertEqual(expected.hour, result.hour)
        self.assertEqual(expected.min, result.min)


if __name__ == "__main__":
    unittest.main()