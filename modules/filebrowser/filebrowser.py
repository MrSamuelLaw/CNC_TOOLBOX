#!/usr/bin/env python3

# TODO:
#   set up the current_directory as a property

from pathlib import Path, PurePath
from typing import Tuple, List


class FileBrowser():
    """Backend implimentation for a filebrowser"""

    # class variables
    _default_dir = Path.cwd()

    def __init__(self, path: Path = None) -> None:
        # instance variables
        self.curdir = path if path is not None else self._default_dir

    @property
    def curdir(self) -> None:
        """Using the property decorator here allows
        for all instances of the FileBrowser class to
        share the defualt directory property. It behaves
        the same as the browser on Windows where it opens
        up where you had it last."""
        pass

    @curdir.setter
    def curdir(self, path: Path) -> None:
        if Path(path).is_dir():
            self._curdir = path
            FileBrowser._default_dir = path
        else:
            raise ValueError("path is not a directory")

    @curdir.getter
    def curdir(self) -> Path:
        return self._curdir

    def list_dir(self, path_like: Path) -> Tuple[List[str], List[str]]:
        """Takes a path like object as a string
        and returns a snapshot of the directory if its
        a folder"""
        # ensure path object
        path_object = Path(path_like)
        # list files if directory
        if path_object.is_dir():
            self.curdir = path_object
            files = [f for f in path_object.iterdir() if f.is_file()]
            folders = [f for f in path_object.iterdir() if f.is_dir()]
            return (files, folders)
        # raise errors if anything else
        elif path_object.is_file():
            raise ValueError("path is file not directory")
        else:
            raise ValueError("path is not directory or file")

    def up_one(self) -> Tuple[List[str], List[str]]:
        """Traverses up one in the file directory"""
        if self.curdir.parent != self.curdir:
            self.curdir = self.curdir.parent
            files = [f for f in self.curdir.iterdir() if f.is_file()]
            folders = [f for f in self.curdir.iterdir() if f.is_dir()]
            return (files, folders)
        else:
            raise ValueError("current directory is root")
