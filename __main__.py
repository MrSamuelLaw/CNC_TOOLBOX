#!/usr/bin/env python3

import sys
from pathlib import Path
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from modules.filebrowser import QmlFileBrowser


if __name__ == "__main__":
    # cmd line args
    sys.argv += ["--platform", "windows:darkmode=2"]  # make dark mode
    # enable what you see is what you get from qt designer
    QQuickStyle.setStyle("Basic")

    # top level objects
    app = QGuiApplication(sys.argv)                   # create the app
    engine = QQmlApplicationEngine()                  # create the engine

    # exposeing python object to qml
    context = engine.rootContext()        # context object
    fb = QmlFileBrowser()                 # create QFileBrowser
    context.setContextProperty("fb", fb)  # expose fb Slots to qml
    engine.addImageProvider("fb", fb)     # expose fb requestPixmap

    # component loading
    url = Path.joinpath(Path(__file__).parent, "qml")  # set the path
    engine.load(str(url.joinpath("FileBrowser.qml")))  # load the components

    # run the app
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
