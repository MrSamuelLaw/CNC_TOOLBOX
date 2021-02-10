import unittest
from modules.filebrowser import QmlFileBrowser
from PySide6.QtGui import QGuiApplication


class TestQmlFileBrowser(unittest.TestCase):

    def test_current_directory(self):
        # create objects
        qfb = QmlFileBrowser()  # child object
        fb = qfb.fb             # parent object
        # create path from json
        path = qfb.json_2_path(qfb.curdir())
        # compare
        self.assertEqual(str(fb.curdir), str(path))

    def test_requestPixmap(self):
        app = QGuiApplication()
        qfb = QmlFileBrowser()
        pm = qfb.requestPixmap(str(__file__))
        print(pm)


if __name__ == "__main__":
    unittest.main()
