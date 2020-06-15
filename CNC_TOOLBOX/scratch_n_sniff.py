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
exe_path = path.join(start_dir, '.venv', 'Scripts', 'python.exe')

skips = ['.venv']  # skip tests in these dirs.
onlys = ['shop_bot']  # if not empty, will run only these test folders

for root, dirs, files in walk(start_dir):
    for name in dirs:
        if (name == "test"):  # loop through and find test files
            test_folder = path.join(root, name)
            # make sure tests are not in directories to skip
            if not any([s for s in skips if s in test_folder]):
                if onlys and not any([o for o in onlys if o in test_folder]):
                    continue
                cmd = [
                    # 'python',
                    exe_path,
                    '-m',
                    'unittest',
                    'discover',
                    '-s',
                    test_folder,
                    # '-v'  # verbose output
                ]
                # run cmd
                results = run(cmd, cwd=root)
