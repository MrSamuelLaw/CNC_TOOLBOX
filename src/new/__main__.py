import asyncio
import delays
from os import chdir
from pathlib import PurePath
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QUrl


async def gui_loop(app: QApplication):
    """"""
    while True:
        app.processEvents()
        await asyncio.sleep(delays.small_delay)



if __name__ == "__main__":
    # set cwd
    chdir(PurePath(__file__).parent)

    # setup the home window
    app = QApplication([])
    view = QQuickView()
    url = QUrl("qml/view.qml")
    view.setSource(url)
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.show()

    # start the loop that contains the application
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gui_loop(app))
