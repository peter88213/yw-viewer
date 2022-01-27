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

    statView (str): String containing the total numbers of chapters, scenes and words.
    descView: (list of tuples): Project description.
    chapterTitles (list of tuples): List of chapter titles.
    chapterDescriptions (list of tuples): Text containing chapter titles and descriptions.
    sceneTitles (list of tuples): Text containing chapter titles and listed scene titles.
    sceneContents (list of tuples): Text containing chapter titles and scene contents.

    (The list entries are tuples containing the text and a formatting tag.)       
    """
    H1_TAG = 'h1'
    H2_TAG = 'h2'
    H3_TAG = 'h3'
    ITALIC_TAG = 'italic'
    BOLD_TAG = 'bold'
    CENTER_TAG = 'center'
    NO_TAG = ''
    SCENE_DIVIDER = ('* * *\n', CENTER_TAG)

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

        self.descView = []

        if self.desc:
            self.descView.append([self.desc, self.NO_TAG])

        else:
            self.descView.append(['(No project description available)', 'italic'])

        self.chapterTitles = []
        self.chapterDescriptions = []
        self.sceneTitles = []
        self.sceneDescriptions = []
        self.sceneContents = []
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
                headingTag = self.H2_TAG
                listTag = self.NO_TAG

            else:
                headingTag = self.H1_TAG
                listTag = self.BOLD_TAG

            # Get chapter titles.

            if self.chapters[chId].title:
                self.chapterTitles.append((self.chapters[chId].title + '\n', listTag))
                sceneHeading = [self.chapters[chId].title + '\n', headingTag]
                self.sceneTitles.append(sceneHeading)

            # Get chapter descriptions.

            if self.chapters[chId].desc:
                self.chapterDescriptions.append((self.chapters[chId].title + '\n', headingTag))
                self.chapterDescriptions.append((self.chapters[chId].desc + '\n', self.NO_TAG))

            for scId in self.chapters[chId].srtScenes:

                if not (self.scenes[scId].isUnused or self.scenes[scId].isNotesScene or self.scenes[scId].isTodoScene):
                    sceneCount += 1

                    # Get scene titles.

                    if self.scenes[scId].title:
                        self.sceneTitles.append((self.scenes[scId].title + '\n', self.NO_TAG))

                    # Get scene descriptions.

                    if self.scenes[scId].desc:
                        self.sceneDescriptions.append(sceneHeading)
                        self.sceneDescriptions.append((self.scenes[scId].desc + '\n', self.NO_TAG))

                    # Get scene contents.

                    if self.scenes[scId].sceneContent:
                        self.sceneContents.append(sceneHeading)
                        self.sceneContents.append((self.convert_from_yw(
                            self.scenes[scId].sceneContent + '\n'), self.NO_TAG))

                    sceneHeading = self.SCENE_DIVIDER

                    # Get scene word count.

                    if self.scenes[scId].wordCount:
                        wordCount += self.scenes[scId].wordCount

        self.statView = str(chapterCount) + ' chapters, ' + str(sceneCount) + ' scenes, ' + str(wordCount) + ' words'

        if len(self.chapterTitles) == 0:
            self.chapterTitles.append(('(No chapter titles available)', self.ITALIC_TAG))

        if len(self.chapterDescriptions) == 0:
            self.chapterDescriptions.append(('(No chapter descriptions available)', self.ITALIC_TAG))

        if len(self.sceneTitles) == 0:
            self.sceneTitles.append(('(No scene titles available)', self.ITALIC_TAG))

        if len(self.sceneDescriptions) == 0:
            self.sceneDescriptions.append(('(No scene descriptions available)', self.ITALIC_TAG))

        if len(self.sceneContents) == 0:
            self.sceneContents.append(('(No scene contents available)', self.ITALIC_TAG))

        return 'SUCCESS'

    def convert_from_yw(self, text):
        """Convert yw7 markup to Markdown.
        """
        return re.sub('\[\/*[i|b|h|c|r|s|u]\d*\]', '', text)
