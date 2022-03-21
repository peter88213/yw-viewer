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
from ywviewerlib.rich_text_tk import RichTextTk


class Yw7ViewerTk(MainTk):
    """A tkinter GUI class for yWriter file viewing.
    
    Public methods:
        open_project(fileName) -- create a yWriter project instance and read the file. 

    Show titles, descriptions, and contents in a text box.
    """

    def __init__(self, title, **kwargs):
        """Put a text box to the GUI main window.
        
        Positional arguments:
            title -- application title to be displayed at the window frame.
         
        Required keyword arguments:
            yw_last_open -- str: initial file.
        
        Extends the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self._textBox = RichTextTk(self._mainWindow, height=20, width=60, spacing1=10, spacing2=2, wrap='word', padx=40)
        self._textBox.pack(expand=True, fill='both')
        self._prjDescription = []
        self._chapterTitles = []
        self._chapterDescriptions = []
        self._sceneTitles = []
        self._sceneDescriptions = []
        self._sceneContents = []

    def _build_main_menu(self):
        """Add main menu entries.
        
        Extends the superclass template method. 
        """
        super()._build_main_menu()
        self._quickViewMenu = tk.Menu(self._mainMenu, title='my title', tearoff=0)
        self._mainMenu.add_cascade(label='Quick view', underline=0, menu=self._quickViewMenu)
        self._mainMenu.entryconfig('Quick view', state='disabled')
        self._quickViewMenu.add_command(label='Project description', underline=0, command=lambda: self._show_text(self._prjDescription))
        self._quickViewMenu.add_command(label='Chapter titles', underline=8, command=lambda: self._show_text(self._chapterTitles))
        self._quickViewMenu.add_command(label='Chapter descriptions', underline=0,
                                       command=lambda: self._show_text(self._chapterDescriptions))
        self._quickViewMenu.add_command(label='Scene titles', underline=7, command=lambda: self._show_text(self._sceneTitles))
        self._quickViewMenu.add_command(label='Scene descriptions', underline=6,
                                       command=lambda: self._show_text(self._sceneDescriptions))
        self._quickViewMenu.add_command(label='Scene contents', underline=7, command=lambda: self._show_text(self._sceneContents))
        self._quickViewMenu.insert_separator(1)
        self._quickViewMenu.insert_separator(4)

    def _disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super()._disable_menu()
        self._mainMenu.entryconfig('Quick view', state='disabled')

    def _enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super()._enable_menu()
        self._mainMenu.entryconfig('Quick view', state='normal')

    def _show_text(self, taggedText):
        """Load text into the text box.
        
        Positional arguments:
            taggedText -- list of (text, formatting tag) tuples. 
        
        Disable text editing.
        """
        self._textBox['state'] = 'normal'
        self._textBox.delete('1.0', tk.END)
        for text, tag in taggedText:
            self._textBox.insert(tk.END, text, tag)
        self._textBox['state'] = 'disabled'

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.

        Positional arguments:
            fileName -- str: project file path.
            
        Display project title, description and status.
        Create for quick viewing: 
            statView -- str: String containing the total numbers of chapters, scenes and words.
            descView -- list of tuples: Project description.
            _chapterTitles -- list of tuples: List of chapter titles.
            _chapterDescriptions -- list of tuples: Text containing chapter titles and descriptions.
            _sceneTitles -- list of tuples: Text containing chapter titles and listed scene titles.
            _sceneContents -- list of tuples: Text containing chapter titles and scene contents.
        (The list entries are tuples containing the text and a formatting tag.)       
        
        Return True on success, otherwise return False.
        Extends the superclass method.
        """

        def convert_from_yw(text):
            """Remove yw7 markup from text."""
            return re.sub('\[\/*[i|b|h|c|r|s|u]\d*\]', '', text)

        if not super().open_project(fileName):
            return False

        # Get project description.
        self._prjDescription = []
        if self.ywPrj.desc:
            self._prjDescription.append((self.ywPrj.desc, ''))
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
        for chId in self.ywPrj.srtChapters:
            if self.ywPrj.chapters[chId].isUnused:
                continue

            if self.ywPrj.chapters[chId].chType != 0 and self.ywPrj.chapters[chId].oldType != 0:
                continue

            chapterCount += 1
            if self.ywPrj.chapters[chId].chLevel == 0:
                headingTag = RichTextTk.H2_TAG
                listTag = ''
            else:
                headingTag = RichTextTk.H1_TAG
                listTag = RichTextTk.BOLD_TAG

            # Get chapter titles.
            if self.ywPrj.chapters[chId].title:
                self._chapterTitles.append((f'{self.ywPrj.chapters[chId].title}\n', listTag))
                sceneHeading = (f'{self.ywPrj.chapters[chId].title}\n', headingTag)
                self._sceneTitles.append(sceneHeading)

            # Get chapter descriptions.
            if self.ywPrj.chapters[chId].desc:
                self._chapterDescriptions.append((f'{self.ywPrj.chapters[chId].title}\n', headingTag))
                self._chapterDescriptions.append((f'{self.ywPrj.chapters[chId].desc}\n', ''))

            for scId in self.ywPrj.chapters[chId].srtScenes:
                if not (self.ywPrj.scenes[scId].isUnused or self.ywPrj.scenes[scId].isNotesScene or self.ywPrj.scenes[scId].isTodoScene):
                    sceneCount += 1

                    # Get scene titles.
                    if self.ywPrj.scenes[scId].title:
                        self._sceneTitles.append((f'{self.ywPrj.scenes[scId].title}\n', ''))

                    # Get scene descriptions.
                    if self.ywPrj.scenes[scId].desc:
                        self._sceneDescriptions.append(sceneHeading)
                        self._sceneDescriptions.append((f'{self.ywPrj.scenes[scId].desc}\n', ''))

                    # Get scene contents.
                    if self.ywPrj.scenes[scId].sceneContent:
                        self._sceneContents.append(sceneHeading)
                        self._sceneContents.append((convert_from_yw(f'{self.ywPrj.scenes[scId].sceneContent}\n'), ''))
                    sceneHeading = ('* * *\n', RichTextTk.CENTER_TAG)

                    # Get scene word count.
                    if self.ywPrj.scenes[scId].wordCount:
                        wordCount += self.ywPrj.scenes[scId].wordCount
        statView = f'{chapterCount} chapters, {sceneCount} scenes, {wordCount} words'
        if not self._chapterTitles:
            self._chapterTitles.append(('(No chapter titles available)', RichTextTk.ITALIC_TAG))
        if not self._chapterDescriptions:
            self._chapterDescriptions.append(('(No chapter descriptions available)', RichTextTk.ITALIC_TAG))
        if not self._sceneTitles:
            self._sceneTitles.append(('(No scene titles available)', RichTextTk.ITALIC_TAG))
        if not self._sceneDescriptions:
            self._sceneDescriptions.append(('(No scene descriptions available)', RichTextTk.ITALIC_TAG))
        if not self._sceneContents:
            self._sceneContents.append(('(No scene contents available)', RichTextTk.ITALIC_TAG))
        self._show_text(self._prjDescription)
        self.show_status(statView)
        return True

    def _close_project(self, event=None):
        """Clear the text box.
        
        Extends the superclass method.
        """
        super()._close_project()
        self._textBox['state'] = 'normal'
        self._textBox.delete('1.0', tk.END)
        self._textBox['state'] = 'disabled'
