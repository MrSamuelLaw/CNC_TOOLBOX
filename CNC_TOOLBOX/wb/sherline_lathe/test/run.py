#!/usr/bin/env

'''
runs test for local workbench
'''

import unittest
import subprocess
import os


def main():
    if True:
        loader = unittest.TestLoader()
        start_dir = os.getcwd() + '/test'
        all_test = loader.discover(start_dir, pattern='test*.py')
        result = unittest.TestResult()
        for suite in all_test:
            for test in suite:
                test.run(result)

        print(result)
        if len(result.failures):
            for f in result.failures:
                print('\n------------')
                print(f)



if __name__ == "__main__":
    main()
