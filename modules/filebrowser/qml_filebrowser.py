import json
from re import compile
from pathlib import Path
from PySide6.QtGui import QPainter, QPixmap, QColor
from PySide6.QtCore import Slot, QFileInfo
from PySide6.QtQuick import QQuickImageProvider
from PySide6.QtWidgets import QFileIconProvider
from modules.filebrowser.filebrowser import FileBrowser
# PySide6 bug workaround


class QmlFileBrowser(QQuickImageProvider):
    """Bridge between the FileBrowser class and the front end
    which written in qml. This class should only enable the
    transfer of data to and from the FileBrowser class, if one
    wishes to extend the FileBrowser class' basic functionality,
    this is not the right spot."""

    def __init__(self):
        # inheriting from QQuickImageProvider also inherits from QObject
        QQuickImageProvider.__init__(self, QQuickImageProvider.Pixmap)

        # objects for which this class acts as a bridge
        self.fb = FileBrowser()
        self.fib = QFileIconProvider()

    @Slot(result=str)
    def curdir(self) -> str:
        """Returns a path object
        with name, and path attributes"""
        return json.dumps(
            self.fb.curdir,
            default=self.path_2_json
        )

    @Slot(str, result=str)
    def dir(self, path: str) -> str:
        """Returns a json string
        with name, path, and suffix attributes"""
        return json.dumps(
            self.fb.dir(path),        # object to convert to json
            default=self.path_2_json  # json hook
        )

    @Slot(str, result=str)
    def parent(self, path: str) -> str:
        """Returns the json for the parent
        of the path argument"""
        path_object = Path(path)
        return json.dumps(
            path_object.parent,       # object to convert to json
            default=self.path_2_json  # json hook
        )

    def requestPixmap(self, id: str, *args) -> QPixmap:
        """Uses the qml desktop api to allow the system to
        return the icon for us, providing a native feel on
        all platforms."""

        p = compile("%5C")                                # "/" are coming in as "%5C"
        id = p.sub("/", id)                               # use regex to fix it
        icon = QFileIconProvider().icon(QFileInfo(id))    # create the icon
        s = icon.availableSizes()[0]                      # get the smallest available size
        pixmap = QPixmap(s)                               # create a pixmap the same size
        pixmap.fill(QColor("transparent"))                # fill the background transparent
        painter = QPainter(pixmap)                        # create the painter with pixmap paint device
        icon.paint(painter, 0, 0, s.width(), s.height())  # call the icon to paint with painter object
        return pixmap

        # Note the bug in PySide6 pixmap()
        # pm = icon.pixmap(size)  // returns a null pixmap

    # ============ json hooks ============
    def path_2_json(self, path: Path) -> str:
        """Converts path object to json"""
        return {
            "name": str(path.name),
            "path": str(path),
            "suffix": str(path.suffix),
            "is_dir": bool(path.is_dir()),
            "is_file": bool(path.is_file()),
        }

    def json_2_path(self, json_: str) -> Path:
        """Converts json representing a path
        into a Path object"""
        obj = json.loads(json_)
        return Path(obj["path"])
