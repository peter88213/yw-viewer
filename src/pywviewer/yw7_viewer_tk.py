#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import re
import tkinter as tk
from tkinter import scrolledtext

from pywriter.pywriter_globals import ERROR
from pywriter.yw.yw7_file import Yw7File
from pywriter.ui.main_tk import MainTk
from pywviewer.rich_text_tk import RichTextTk


class Yw7ViewerTk(MainTk):
    """A tkinter GUI class for yWriter file viewing.

    Show titles, descriptions, and contents in a text box.
    """

    def __init__(self, title, **kwargs):
        """Put a text box to the GUI main window.
        Extend the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self._textBox = RichTextTk(self._mainWindow,  height=20, width=60, spacing1=10, spacing2=2, wrap='word', padx=40)
        self._textBox.pack(expand=True, fill='both')
        self._prjDescription = []
        self._chapterTitles = []
        self._chapterDescriptions = []
        self._sceneTitles = []
        self._sceneDescriptions = []
        self._sceneContents = []

    def _extend_menu(self):
        """Add main menu entries.
        Override the superclass template method. 
        """
        self._quickViewMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Quick view', menu=self._quickViewMenu)
        self._mainMenu.entryconfig('Quick view', state='disabled')
        self._quickViewMenu.add_command(label='Project description', command=lambda: self._show_text(self._prjDescription))
        self._quickViewMenu.add_command(label='Chapter titles', command=lambda: self._show_text(self._chapterTitles))
        self._quickViewMenu.add_command(label='Chapter descriptions',
                                       command=lambda: self._show_text(self._chapterDescriptions))
        self._quickViewMenu.add_command(label='Scene titles', command=lambda: self._show_text(self._sceneTitles))
        self._quickViewMenu.add_command(label='Scene descriptions',
                                       command=lambda: self._show_text(self._sceneDescriptions))
        self._quickViewMenu.add_command(label='Scene contents', command=lambda: self._show_text(self._sceneContents))
        self._quickViewMenu.insert_separator(1)
        self._quickViewMenu.insert_separator(4)

    def _disable_menu(self):
        """Disable menu entries when no project is open.
        Extend the superclass method.      
        """
        super()._disable_menu()
        self._mainMenu.entryconfig('Quick view', state='disabled')

    def _enable_menu(self):
        """Enable menu entries when a project is open.
        Extend the superclass method.
        """
        super()._enable_menu()
        self._mainMenu.entryconfig('Quick view', state='normal')

    def _show_text(self, text):
        """Load text into the text box.
        Disable text editing.
        """
        self._textBox['state'] = 'normal'
        self._textBox.delete('1.0', tk.END)

        for paragraph in text:
            self._textBox.insert(tk.END, paragraph[0], paragraph[1])

        self._textBox['state'] = 'disabled'

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        Display project title, description and status.
        Extend the superclass method.

        Create for quick viewing: 

        statView (str): String containing the total numbers of chapters, scenes and words.
        descView: (list of tuples): Project description.
        _chapterTitles (list of tuples): List of chapter titles.
        _chapterDescriptions (list of tuples): Text containing chapter titles and descriptions.
        _sceneTitles (list of tuples): Text containing chapter titles and listed scene titles.
        _sceneContents (list of tuples): Text containing chapter titles and scene contents.

        (The list entries are tuples containing the text and a formatting tag.)       
        """

        def convert_from_yw(text):
            """Remove yw7 markup."""
            return re.sub('\[\/*[i|b|h|c|r|s|u]\d*\]', '', text)

        fileName = super().open_project(fileName)

        if not fileName:
            return ''

        self._ywPrj = Yw7File(fileName)
        message = self._ywPrj.read()

        if message.startswith(ERROR):
            self._close_project()
            self.set_info_how(message)
            return ''

        if self._ywPrj.title:
            titleView = self._ywPrj.title

        else:
            titleView = 'Untitled yWriter project'

        if self._ywPrj.author:
            authorView = self._ywPrj.author

        else:
            authorView = 'Unknown author'

        self._titleBar.config(text=f'{titleView} by {authorView}')

        # Get project description.

        self._prjDescription = []

        if self._ywPrj.desc:
            self._prjDescription.append((self._ywPrj.desc, ''))

        else:
            self._prjDescription.append(('(No project description available)', 'italic'))

        self._chapterTitles = []
        self._chapterDescriptions = []
        self._sceneTitles = []
        self._sceneDescriptions = []
        self._sceneContents = []
        chapterCount = 0
        sceneCount = 0
        wordCount = 0

        for chId in self._ywPrj.srtChapters:

            if self._ywPrj.chapters[chId].isUnused:
                continue

            if self._ywPrj.chapters[chId].chType != 0 and self._ywPrj.chapters[chId].oldType != 0:
                continue

            chapterCount += 1

            if self._ywPrj.chapters[chId].chLevel == 0:
                headingTag = RichTextTk.H2_TAG
                listTag = ''

            else:
                headingTag = RichTextTk.H1_TAG
                listTag = RichTextTk.BOLD_TAG

            # Get chapter titles.

            if self._ywPrj.chapters[chId].title:
                self._chapterTitles.append((f'{self._ywPrj.chapters[chId].title}\n', listTag))
                sceneHeading = (f'{self._ywPrj.chapters[chId].title}\n', headingTag)
                self._sceneTitles.append(sceneHeading)

            # Get chapter descriptions.

            if self._ywPrj.chapters[chId].desc:
                self._chapterDescriptions.append((f'{self._ywPrj.chapters[chId].title}\n', headingTag))
                self._chapterDescriptions.append((f'{self._ywPrj.chapters[chId].desc}\n', ''))

            for scId in self._ywPrj.chapters[chId].srtScenes:

                if not (self._ywPrj.scenes[scId].isUnused or self._ywPrj.scenes[scId].isNotesScene or self._ywPrj.scenes[scId].isTodoScene):
                    sceneCount += 1

                    # Get scene titles.

                    if self._ywPrj.scenes[scId].title:
                        self._sceneTitles.append((f'{self._ywPrj.scenes[scId].title}\n', ''))

                    # Get scene descriptions.

                    if self._ywPrj.scenes[scId].desc:
                        self._sceneDescriptions.append(sceneHeading)
                        self._sceneDescriptions.append((f'{self._ywPrj.scenes[scId].desc}\n', ''))

                    # Get scene contents.

                    if self._ywPrj.scenes[scId].sceneContent:
                        self._sceneContents.append(sceneHeading)
                        self._sceneContents.append((convert_from_yw(f'{self._ywPrj.scenes[scId].sceneContent}\n'), ''))

                    sceneHeading = ('* * *\n', RichTextTk.CENTER_TAG)

                    # Get scene word count.

                    if self._ywPrj.scenes[scId].wordCount:
                        wordCount += self._ywPrj.scenes[scId].wordCount

        statView = f'{chapterCount} chapters, {sceneCount} scenes, {wordCount} words'

        if len(self._chapterTitles) == 0:
            self._chapterTitles.append(('(No chapter titles available)', RichTextTk.ITALIC_TAG))

        if len(self._chapterDescriptions) == 0:
            self._chapterDescriptions.append(('(No chapter descriptions available)', RichTextTk.ITALIC_TAG))

        if len(self._sceneTitles) == 0:
            self._sceneTitles.append(('(No scene titles available)', RichTextTk.ITALIC_TAG))

        if len(self._sceneDescriptions) == 0:
            self._sceneDescriptions.append(('(No scene descriptions available)', RichTextTk.ITALIC_TAG))

        if len(self._sceneContents) == 0:
            self._sceneContents.append(('(No scene contents available)', RichTextTk.ITALIC_TAG))

        self._show_text(self._prjDescription)
        self._set_status(statView)
        self._enable_menu()

    def _close_project(self):
        """Clear the text box.
        Extend the superclass method.
        """
        super()._close_project()
        self._textBox['state'] = 'normal'
        self._textBox.delete('1.0', tk.END)
        self._textBox['state'] = 'disabled'
