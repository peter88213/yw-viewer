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
        self.textBox = RichTextTk(self.mainWindow,  height=20, width=60, spacing1=10, spacing2=2, wrap='word', padx=40)
        self.textBox.pack(expand=True, fill='both')
        self.prjDescription = []
        self.chapterTitles = []
        self.chapterDescriptions = []
        self.sceneTitles = []
        self.sceneDescriptions = []
        self.sceneContents = []

    def extend_menu(self):
        """Add main menu entries.
        Override the superclass template method. 
        """
        self.quickViewMenu = tk.Menu(self.mainMenu, title='my title', tearoff=0)
        self.mainMenu.add_cascade(label='Quick view', menu=self.quickViewMenu)
        self.mainMenu.entryconfig('Quick view', state='disabled')
        self.quickViewMenu.add_command(label='Project description', command=lambda: self.show_text(self.prjDescription))
        self.quickViewMenu.add_command(label='Chapter titles', command=lambda: self.show_text(self.chapterTitles))
        self.quickViewMenu.add_command(label='Chapter descriptions',
                                       command=lambda: self.show_text(self.chapterDescriptions))
        self.quickViewMenu.add_command(label='Scene titles', command=lambda: self.show_text(self.sceneTitles))
        self.quickViewMenu.add_command(label='Scene descriptions',
                                       command=lambda: self.show_text(self.sceneDescriptions))
        self.quickViewMenu.add_command(label='Scene contents', command=lambda: self.show_text(self.sceneContents))
        self.quickViewMenu.insert_separator(1)
        self.quickViewMenu.insert_separator(4)

    def disable_menu(self):
        """Disable menu entries when no project is open.
        Extend the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig('Quick view', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        Extend the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig('Quick view', state='normal')

    def show_text(self, text):
        """Load text into the text box.
        Disable text editing.
        """
        self.textBox['state'] = 'normal'
        self.textBox.delete('1.0', tk.END)

        for paragraph in text:
            self.textBox.insert(tk.END, paragraph[0], paragraph[1])

        self.textBox['state'] = 'disabled'

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        Display project title, description and status.
        Extend the superclass method.

        Create for quick viewing: 

        statView (str): String containing the total numbers of chapters, scenes and words.
        descView: (list of tuples): Project description.
        chapterTitles (list of tuples): List of chapter titles.
        chapterDescriptions (list of tuples): Text containing chapter titles and descriptions.
        sceneTitles (list of tuples): Text containing chapter titles and listed scene titles.
        sceneContents (list of tuples): Text containing chapter titles and scene contents.

        (The list entries are tuples containing the text and a formatting tag.)       
        """

        def convert_from_yw(text):
            """Remove yw7 markup."""
            return re.sub('\[\/*[i|b|h|c|r|s|u]\d*\]', '', text)

        fileName = super().open_project(fileName)

        if not fileName:
            return ''

        self.ywPrj = Yw7File(fileName)
        message = self.ywPrj.read()

        if message.startswith(ERROR):
            self.close_project()
            self.set_info_how(message)
            return ''

        if self.ywPrj.title:
            titleView = self.ywPrj.title

        else:
            titleView = 'Untitled yWriter project'

        if self.ywPrj.author:
            authorView = self.ywPrj.author

        else:
            authorView = 'Unknown author'

        self.titleBar.config(text=f'{titleView} by {authorView}')

        # Get project description.

        self.prjDescription = []

        if self.ywPrj.desc:
            self.prjDescription.append((self.ywPrj.desc, ''))

        else:
            self.prjDescription.append(('(No project description available)', 'italic'))

        self.chapterTitles = []
        self.chapterDescriptions = []
        self.sceneTitles = []
        self.sceneDescriptions = []
        self.sceneContents = []
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
                self.chapterTitles.append((f'{self.ywPrj.chapters[chId].title}\n', listTag))
                sceneHeading = (f'{self.ywPrj.chapters[chId].title}\n', headingTag)
                self.sceneTitles.append(sceneHeading)

            # Get chapter descriptions.

            if self.ywPrj.chapters[chId].desc:
                self.chapterDescriptions.append((f'{self.ywPrj.chapters[chId].title}\n', headingTag))
                self.chapterDescriptions.append((f'{self.ywPrj.chapters[chId].desc}\n', ''))

            for scId in self.ywPrj.chapters[chId].srtScenes:

                if not (self.ywPrj.scenes[scId].isUnused or self.ywPrj.scenes[scId].isNotesScene or self.ywPrj.scenes[scId].isTodoScene):
                    sceneCount += 1

                    # Get scene titles.

                    if self.ywPrj.scenes[scId].title:
                        self.sceneTitles.append((f'{self.ywPrj.scenes[scId].title}\n', ''))

                    # Get scene descriptions.

                    if self.ywPrj.scenes[scId].desc:
                        self.sceneDescriptions.append(sceneHeading)
                        self.sceneDescriptions.append((f'{self.ywPrj.scenes[scId].desc}\n', ''))

                    # Get scene contents.

                    if self.ywPrj.scenes[scId].sceneContent:
                        self.sceneContents.append(sceneHeading)
                        self.sceneContents.append((convert_from_yw(f'{self.ywPrj.scenes[scId].sceneContent}\n'), ''))

                    sceneHeading = ('* * *\n', RichTextTk.CENTER_TAG)

                    # Get scene word count.

                    if self.ywPrj.scenes[scId].wordCount:
                        wordCount += self.ywPrj.scenes[scId].wordCount

        self.statView = f'{chapterCount} chapters, {sceneCount} scenes, {wordCount} words'

        if len(self.chapterTitles) == 0:
            self.chapterTitles.append(('(No chapter titles available)', RichTextTk.ITALIC_TAG))

        if len(self.chapterDescriptions) == 0:
            self.chapterDescriptions.append(('(No chapter descriptions available)', RichTextTk.ITALIC_TAG))

        if len(self.sceneTitles) == 0:
            self.sceneTitles.append(('(No scene titles available)', RichTextTk.ITALIC_TAG))

        if len(self.sceneDescriptions) == 0:
            self.sceneDescriptions.append(('(No scene descriptions available)', RichTextTk.ITALIC_TAG))

        if len(self.sceneContents) == 0:
            self.sceneContents.append(('(No scene contents available)', RichTextTk.ITALIC_TAG))

        self.show_text(self.prjDescription)
        self.set_status(self.statView)
        self.enable_menu()

    def close_project(self):
        """Clear the text box.
        Extend the superclass method.
        """
        super().close_project()
        self.textBox['state'] = 'normal'
        self.textBox.delete('1.0', tk.END)
        self.textBox['state'] = 'disabled'
