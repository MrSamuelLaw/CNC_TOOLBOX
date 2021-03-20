import pathlib
from typing import Union
from pydantic.main import BaseModel
from PySide6.QtCore import QObject
from modules.common.decorators import PydanticSlot
from modules.common.models import Response


class FileModel(BaseModel):
    path: pathlib.Path
    text: Union[str, None]


class FileModelResponse(Response):
    text: Union[str, None]


class QMLFileHandler(QObject):
    """The QMLFileHandler is the bridge between
    the front end and the FileHandler class. What this means is
    that the QMLFileHandler class should not have any implimentation
    functions, but rather execution functions, where it executes
    code using the implimentations that are in other classes."""

    def __init__(self):
        super().__init__()

    @PydanticSlot(model=FileModel)
    def read_text_file(self, file: FileModel) -> FileModelResponse:
        """Slot for opening text files"""
        try:
            file.text = str(file.path.read_text())
            r = FileModelResponse(
                status=True,
                message="file read successfully",
                text=file.text
            )
        except Exception as e:
            r = FileModelResponse(
                status=False,
                message="\n".join([f"failed to read from file at {file.path}",
                                   f"with the following error:\n{str(e)}"])
            )
        return r

    @PydanticSlot(model=FileModel)
    def write_text_file(self, file: FileModel) -> Response:
        """Slot for opening text files"""
        try:
            file.path.write_text(file.text, 'utf-8')
            r = Response(status=True,
                         message="file written to successfully",)
        except Exception as e:
            r = Response(status=False,
                         message="\n".join([f"failed to write to file at {file.path}",
                                            f"with the following error:\n{str(e)}"]))
        return r
