#!/usr/bin/env python3
"""yWriter file viewer. 

Version @release

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
import argparse
from pathlib import Path

from pywriter.config.configuration import Configuration
from pywviewer.file_viewer import FileViewer

APPNAME = 'yw-viewer'

SETTINGS = dict(
    yw_last_open='',
)

OPTIONS = {}


def run(sourcePath, installDir=''):

    #--- Load configuration

    sourceDir = os.path.dirname(sourcePath)

    if sourceDir == '':
        sourceDir = './'

    else:
        sourceDir += '/'

    iniFile = installDir + APPNAME + '.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    kwargs = {}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    viewerUi = FileViewer(fileName=sourcePath, title='yw-viewer @release', **kwargs)
    viewerUi.run()

    #--- Save project specific configuration

    for keyword in viewerUi.kwargs:

        if keyword in configuration.options:
            configuration.options[keyword] = viewerUi.kwargs[keyword]

        elif keyword in configuration.settings:
            configuration.settings[keyword] = viewerUi.kwargs[keyword]

        configuration.write(iniFile)


if __name__ == '__main__':

    try:
        installDir = str(Path.home()).replace('\\', '/') + '/.pywriter/' + APPNAME + '/config/'

    except:
        installDir = ''

    os.makedirs(installDir, exist_ok=True)

    if len(sys.argv) == 1:
        run('', installDir)

    else:
        parser = argparse.ArgumentParser(
            description='yWriter file viewer',
            epilog='')
        parser.add_argument('sourcePath',
                            metavar='Sourcefile',
                            help='The path of the yWriter project file.')

        args = parser.parse_args()
        run(args.sourcePath, installDir)
