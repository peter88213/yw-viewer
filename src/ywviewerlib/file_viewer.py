""""Provide a tkinter text box class for file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
import tkinter as tk
from pywriter.pywriter_globals import *
from pywriter.ui.rich_text_tk import RichTextTk


class FileViewer:
    """A tkinter text box class for yWriter file viewing.
    
    Public methods:
        view_text(taggedText) -- load tagged text into the text box.
        build_views() -- create tagged text for quick viewing.
        reset_view() -- clear the text box.

    Public instance variables:
        prjDescription -- list of tuples: Project description.
        chapterTitles -- list of tuples: List of chapter titles.
        chapterDescriptions -- list of tuples: Text containing chapter titles and descriptions.
        sceneTitles -- list of tuples: Text containing chapter titles and listed scene titles.
        sceneDescriptions -- list of tuples: Text containing chapter titles and scene descriptions.
        sceneContents -- list of tuples: Text containing chapter titles and scene contents.

    Show titles, descriptions, and contents in a text box.
    """

    def __init__(self, ui):
        """Put a text box to the GUI main window.
        
        Positional arguments:
            title -- application title to be displayed at the window frame.
         
        Required keyword arguments:
            yw_last_open -- str: initial file.
        
        Extends the superclass constructor.
        """
        self._ui = ui
        self._textBox = RichTextTk(self._ui.viewerWindow, height=20, width=60, spacing1=10, spacing2=2, wrap='word', padx=40)
        self._textBox.pack(expand=True, fill='both')
        self.prjDescription = []
        self.chapterTitles = []
        self.chapterDescriptions = []
        self.sceneTitles = []
        self.sceneDescriptions = []
        self.sceneContents = []

    def view_text(self, taggedText):
        """Load tagged text into the text box.
        
        Positional arguments:
            taggedText -- list of (text, formatting tag) tuples. 
        
        Disable text editing.
        """
        self._textBox['state'] = 'normal'
        self._textBox.delete('1.0', tk.END)
        for text, tag in taggedText:
            self._textBox.insert(tk.END, text, tag)
        self._textBox['state'] = 'disabled'

    def build_views(self):
        """Create tagged text for quick viewing.
         
        Return a string containing the total numbers of chapters, scenes and words.
        """

        def convert_from_yw(text):
            """Remove yw7 markup from text."""
            return re.sub(r'\[\/*[i|b|h|c|r|s|u]\d*\]', '', text)

        # Get project description.
        self.prjDescription = []
        if self._ui.novel.desc:
            self.prjDescription.append((self._ui.novel.desc, ''))
        else:
            self.prjDescription.append((f'({_("No project description available")})', 'italic'))
        self.chapterTitles = []
        self.chapterDescriptions = []
        self.sceneTitles = []
        self.sceneDescriptions = []
        self.sceneContents = []
        chapterCount = 0
        sceneCount = 0
        wordCount = 0
        for chId in self._ui.novel.srtChapters:
            if self._ui.novel.chapters[chId].chType != 0:
                continue

            chapterCount += 1
            if self._ui.novel.chapters[chId].chLevel == 0:
                headingTag = RichTextTk.H2_TAG
                listTag = ''
            else:
                headingTag = RichTextTk.H1_TAG
                listTag = RichTextTk.BOLD_TAG

            # Get chapter titles.
            if self._ui.novel.chapters[chId].title:
                self.chapterTitles.append((f'{self._ui.novel.chapters[chId].title}\n', listTag))
                sceneHeading = (f'{self._ui.novel.chapters[chId].title}\n', headingTag)
                self.sceneTitles.append(sceneHeading)

            # Get chapter descriptions.
            if self._ui.novel.chapters[chId].desc:
                self.chapterDescriptions.append((f'{self._ui.novel.chapters[chId].title}\n', headingTag))
                self.chapterDescriptions.append((f'{self._ui.novel.chapters[chId].desc}\n', ''))

            for scId in self._ui.novel.chapters[chId].srtScenes:
                if self._ui.novel.scenes[scId].scType == 0:
                    sceneCount += 1

                    # Get scene titles.
                    if self._ui.novel.scenes[scId].title:
                        self.sceneTitles.append((f'{self._ui.novel.scenes[scId].title}\n', ''))

                    # Get scene descriptions.
                    if self._ui.novel.scenes[scId].desc:
                        self.sceneDescriptions.append(sceneHeading)
                        self.sceneDescriptions.append((f'{self._ui.novel.scenes[scId].desc}\n', ''))

                    # Get scene contents.
                    if self._ui.novel.scenes[scId].sceneContent:
                        self.sceneContents.append(sceneHeading)
                        self.sceneContents.append((convert_from_yw(f'{self._ui.novel.scenes[scId].sceneContent}\n'), ''))
                    sceneHeading = ('* * *\n', RichTextTk.CENTER_TAG)

                    # Get scene word count.
                    if self._ui.novel.scenes[scId].wordCount:
                        wordCount += self._ui.novel.scenes[scId].wordCount
        if not self.chapterTitles:
            self.chapterTitles.append((f'{_("No chapter titles available")})', RichTextTk.ITALIC_TAG))
        if not self.chapterDescriptions:
            self.chapterDescriptions.append((f'({_("No chapter descriptions available")})', RichTextTk.ITALIC_TAG))
        if not self.sceneTitles:
            self.sceneTitles.append((f'{_("No scene titles available")})', RichTextTk.ITALIC_TAG))
        if not self.sceneDescriptions:
            self.sceneDescriptions.append((f'({_("No scene descriptions available")})', RichTextTk.ITALIC_TAG))
        if not self.sceneContents:
            self.sceneContents.append((f'({_("No scene contents available")})', RichTextTk.ITALIC_TAG))
        return f'{chapterCount} {_("chapters")}, {sceneCount} {_("scenes")}, {wordCount} {_("words")}'

    def reset_view(self):
        """Clear the text box."""
        self._textBox['state'] = 'normal'
        self._textBox.delete('1.0', tk.END)
        self._textBox['state'] = 'disabled'
