#!/usr/bin/env python3

""" script for recursive test finding and running """

from os import walk, getcwd, path
from subprocess import run

"""
finds tests by iterating through and finding all folders
labeled test. WILL stop on breakpoint() and turn the terminal
into an interactive debugger.

cwd = where the user files are located
      that test files are testing
"""

start_dir = getcwd()

for root, dirs, files in walk(start_dir):
    for name in dirs:
        if name == "test":
            test_folder = path.join(root, name)
            cmd = ['python','-m','unittest','discover','-s',test_folder]
            results = run(cmd, cwd=root)
