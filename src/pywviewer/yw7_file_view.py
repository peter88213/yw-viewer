"""Provide a class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import re

from pywriter.yw.yw7_file import Yw7File


class Yw7FileView(Yw7File):
    """A class for yWriter file viewing.

    Extend the superclass by information for quick project viewing:

    Public instance variables:

    descView (str): Markdown formatted project description.
    chapterTitles (str): Markdown formatted list of chapter titles.
    chapterDescriptions (str): Markdown formatted text containing chapter titles and descriptions.
    sceneTitles (str): Markdown formatted text containing chapter titles and listed scene titles.
    sceneContents (str): Markdown formatted text containing chapter titles and scene contents.
    statView (str): String containing the total numbers of chapters, scenes and words.
    """

    SCENE_DIVIDER = '\t* * *'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables:
        Extend the superclass constructor by adding viewer information.
        """
        super().__init__(filePath)
        self.chapterTitles = None
        self.chapterDescriptions = None
        self.sceneTitles = None
        self.sceneDescriptions = None
        self.sceneContents = None
        self.statView = None
        self.descView = None

    def read(self):
        """Extend the superclass by creating viewer information.
        """
        message = super().read()

        if message.startswith('ERROR'):
            return message

        # Get project description.

        if self.desc:
            self.descView = self.convert_from_yw(self.desc)

        else:
            self.descView = '(No project description available)'

        chapterTitles = []
        chapterDescriptions = []
        sceneTitles = []
        sceneDescriptions = []
        sceneContents = []
        chapterCount = 0
        sceneCount = 0
        wordCount = 0

        for chId in self.srtChapters:

            if self.chapters[chId].isUnused:
                continue

            if self.chapters[chId].chType != 0 and self.chapters[chId].oldType != 0:
                continue

            chapterCount += 1

            if self.chapters[chId].chLevel == 0:
                headingPrefix = '## '

            else:
                headingPrefix = '# '

            # Get chapter titles.

            if self.chapters[chId].title:
                chapterTitles.append('- ' + self.chapters[chId].title)
                sceneHeading = '\n' + headingPrefix + self.chapters[chId].title + '\n'
                sceneTitles.append(sceneHeading)

            # Get chapter descriptions.

            if self.chapters[chId].desc:
                chapterDescriptions.append('\n' + headingPrefix + self.chapters[chId].title + '\n')
                chapterDescriptions.append(self.convert_from_yw(self.chapters[chId].desc))

            for scId in self.chapters[chId].srtScenes:

                if not (self.scenes[scId].isUnused or self.scenes[scId].isNotesScene or self.scenes[scId].isTodoScene):
                    sceneCount += 1

                    # Get scene titles.

                    if self.scenes[scId].title:
                        sceneTitles.append('- ' + self.scenes[scId].title)

                    # Get scene descriptions.

                    if self.scenes[scId].desc:
                        sceneDescriptions.append(sceneHeading)
                        sceneDescriptions.append(self.convert_from_yw(self.scenes[scId].desc))

                    # Get scene contents.

                    if self.scenes[scId].sceneContent:
                        sceneContents.append(sceneHeading)
                        sceneContents.append(self.convert_from_yw(self.scenes[scId].sceneContent))

                    sceneHeading = self.SCENE_DIVIDER

                    # Get scene word count.

                    if self.scenes[scId].wordCount:
                        wordCount += self.scenes[scId].wordCount

        self.statView = str(chapterCount) + ' chapters, ' + str(sceneCount) + ' scenes, ' + str(wordCount) + ' words'

        self.chapterTitles = '\n'.join(chapterTitles)

        if not self.chapterTitles:
            self.chapterTitles = '(No chapter titles available)'

        self.chapterDescriptions = '\n\n'.join(chapterDescriptions)

        if not self.chapterDescriptions:
            self.chapterDescriptions = '(No chapter descriptions available)'

        self.sceneTitles = '\n'.join(sceneTitles)

        if not self.sceneTitles:
            self.sceneTitles = '(No scene titles available)'

        self.sceneDescriptions = '\n\n'.join(sceneDescriptions)

        if not self.sceneDescriptions:
            self.sceneDescriptions = '(No scene descriptions available)'

        self.sceneContents = '\n\n'.join(sceneContents)

        if not self.sceneContents:
            self.sceneContents = '(No scene contents available)'

        return 'SUCCESS'

    def convert_from_yw(self, text):
        """Convert yw7 markup to Markdown.
        """

        MD_REPLACEMENTS = [
            ['\n', '\n\n'],
            ['[i] ', ' [i]'],
            ['[b] ', ' [b]'],
            ['[s] ', ' [s]'],
            ['[i]', '*'],
            ['[/i]', '*'],
            ['[b]', '**'],
            ['[/b]', '**'],
            ['/*', '<!---'],
            ['*/', '--->'],
            ['  ', ' '],
        ]

        try:

            for r in MD_REPLACEMENTS:
                text = text.replace(r[0], r[1])

            text = re.sub('\[\/*[h|c|r|s|u]\d*\]', '', text)
            # Remove highlighting, alignment, and underline tags

        except AttributeError:
            text = ''

        return text
