#!./.venv/Scripts/pythonw.exe

import sys
from pathlib import Path
from PySide6.QtQml import QQmlDebuggingEnabler
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtGui import QGuiApplication, Qt
from PySide6.QtQml import QQmlApplicationEngine
from pydantic.main import BaseModel
from modules.file_handling import QMLFileHandler
from modules.sherline_lathe import QMLToolTableGenerator
from pydantic.schema import schema


if __name__ == "__main__":
    # uncomment these two lines to enable qml debugging
    debug_enabler = QQmlDebuggingEnabler()
    # sys.argv += ["-qmljsdebugger=port:1234,block"]

    # cmd line args
    sys.argv += ["--platform", "windows:darkmode=2"]  # make dark mode
    # enable what you see is what you get from qt designer
    QQuickStyle.setStyle("Basic")
    # enable qml debugger

    # top level objects
    QGuiApplication.setAttribute(Qt.AA_UseDesktopOpenGL)      # specify how to render
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # enable high dpi
    app = QGuiApplication(sys.argv)   # create the app
    engine = QQmlApplicationEngine()  # create the engine

    # exposeing python object to qml
    context = engine.rootContext()                          # context object
    filehandler = QMLFileHandler()                          # create QMLFileHandler
    tool_table_generator = QMLToolTableGenerator()          # create QMLToolTableGenerator
    context.setContextProperty("filehandler", filehandler)                    # expose QMLFileHandler
    context.setContextProperty("tool_table_generator", tool_table_generator)  # expose QMLFileHandler

    # setup image providers
    # engine.addImageProvider("fb", fb)     # expose fb requestPixmap

    # component loading
    url = Path.joinpath(Path(__file__).parent, "qml")  # set the path
    engine.load(str(url.joinpath("main.qml")))         # load the components

    # run the app
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
