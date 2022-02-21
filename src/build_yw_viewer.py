""" Build a python script for the yw-viewer distribution.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the pywriter package.

The PyWriter project (see see https://github.com/peter88213/PyWriter)
must be located on the same directory level as the yw-viewer project. 

For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys 
sys.path.insert(0, f'{os.getcwd()}/../../PyWriter/src')
import inliner

SRC = '../src/'
BUILD = '../test/'
SOURCE_FILE_GUI = f'{SRC}yw_viewer_.pyw'
TARGET_FILE_GUI = f'{BUILD}yw_viewer.pyw'


def main():
    inliner.run(SOURCE_FILE_GUI, TARGET_FILE_GUI, 'ywviewerlib', '../src/')
    inliner.run(TARGET_FILE_GUI, TARGET_FILE_GUI, 'pywriter', '../../PyWriter/src/')
    print('Done.')


if __name__ == '__main__':
    main()
