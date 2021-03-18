from pathlib import Path
from PySide6.QtCore import QObject, Slot


class QMLFileHandler(QObject):
    """The QMLFileHandler is the bridge between
    the front end and the FileHandler class. What this means is
    that the QMLFileHandler class should not have any implimentation
    functions, but rather execution functions, where it executes
    code using the implimentations that are in other classes."""

    def __init__(self):
        super().__init__()

    @Slot(str, result=str)
    def read_text_file(self, url: str) -> str:
        """Slot for opening text files"""
        file = Path(url)
        text = str(file.read_text())
        return text

    @Slot(str, str)
    def write_text_file(self, url: str, text: str):
        """Slot for opening text files"""
        file = Path(url)
        file.write_text(text, 'utf-8')
