#!/usr/bin/env python3

from pathlib import Path
from typing import Union
from datetime import datetime


class FileBrowser():
    """Backend implimentation for a filebrowser
    the property curdir works using strings
    to access the underlying path object, use
    the _curdir attribute"""

    # class variables
    _default_dir_object = Path.cwd()
    _timestamp_format = "%I:%M%p - %m/%d/%Y"

    def __init__(self) -> None:
        super().__init__()
        self.curdir = FileBrowser._default_dir_object

    @property
    def curdir(self) -> Path:
        return self._curdir_object

    @curdir.setter
    def curdir(self, url: Union[str, Path]) -> None:
        path = Path(url)                            # convert string to path
        if path.is_dir():                           # check if is directory
            self._curdir_object = path              # update instance value
            FileBrowser._default_dir_object = path  # update class value
        else:
            raise ValueError("path is not a directory")

    def dir(self, path: Union[str, Path]) -> dict:
        """Takes a path like object as a string
        and returns a snapshot of the directory if its
        a folder"""
        path_object = Path(path)                        # convert to path is possible
        if path_object.is_dir():                        # list files if directory if possible
            self.curdir = path_object                   # update classes position
            items = [f for f in path_object.iterdir()]  # create a list of Path objects
            return items
        # raise errors if anything else
        elif path_object.is_file():
            raise ValueError("path is file not directory")
        else:
            raise ValueError("path is not directory or file")

    def st_mtime_to_string(self, seconds: float) -> str:
        """Converts the float, as returned by st_mtime attribute
        of the pathlib.stat() function, into a string."""
        time = datetime.fromtimestamp(seconds)
        string = time.strftime(self._timestamp_format)
        return string
