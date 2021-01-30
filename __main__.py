#!/usr/bin/env python3

import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from modules.filebrowser import FileBrowser


if __name__ == "__main__":
    sys.argv += ["--platform", "windows:darkmode=2"]      # make dark mode
    app = QGuiApplication(sys.argv)                       # create the app
    engine = QQmlApplicationEngine()                      # create the engine
    url = Path.joinpath(Path(__file__).parent, "qml")     # the path
    engine.load(str(url.joinpath("FileBrowser.qml")))     # load the component

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())

