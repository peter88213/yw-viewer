#!/usr/bin/env python3
""""Provide a class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import re
import tkinter as tk
from tkinter import filedialog, END
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk
from tkinter import scrolledtext

from pywriter.yw.yw7_file import Yw7File


class FileViewer():
    """A class for yWriter file viewing.

    Show titles, descriptions, and contents in a text box.
    """
    SCENE_DIVIDER = '\t* * *'

    def __init__(self, fileName='', title='', **kwargs):
        if fileName:
            self.fileName = fileName

        elif kwargs['yw_last_open']:
            self.fileName = kwargs['yw_last_open']

        else:
            self.fileName = ''

        self.kwargs = kwargs
        self.mainWindow = tk.Tk()
        self.mainWindow.title(title)
        self.init_dir = os.path.dirname(fileName)
        self.novel = None
        self.properties = None
        self.chapterTitles = None
        self.chapterDescriptions = None
        self.sceneTitles = None
        self.sceneDescriptions = None
        self.sceneContents = None

    def open_file(self, fileName=''):

        def convert_from_yw(text):
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

        #--- Begin open_file() method.

        if not fileName:
            fileName = filedialog.askopenfilename(filetypes=[('yWriter 7 project', '.yw7')],
                                                  defaultextension='.yw7', initialdir=self.init_dir)

        if fileName:
            self.kwargs['yw_last_open'] = fileName
            self.novel = Yw7File(fileName)
            self.novel.read()
            self.pathBar.config(text=os.path.normpath(self.fileName))

            # Get the project title.

            if self.novel.title:
                projectTitle = self.novel.title

            else:
                projectTitle = 'Untitled yWriter project'

            if self.novel.author:
                author = self.novel.author

            else:
                author = 'Unknown author'

            self.titleBar.config(text=projectTitle + ' by ' + author)

            # Get project properties.

            properties = []

            properties.append('\n# Description')

            if self.novel.desc:
                properties.append(convert_from_yw(self.novel.desc))

            else:
                properties.append('(No project description available)')

            self.properties = '\n\n'.join(properties)

            self.show_text(self.properties)

            chapterTitles = []
            chapterDescriptions = []
            sceneTitles = []
            sceneDescriptions = []
            sceneContents = []
            chapterCount = 0
            sceneCount = 0
            wordCount = 0

            for chId in self.novel.srtChapters:

                if self.novel.chapters[chId].isUnused:
                    continue

                if self.novel.chapters[chId].chType != 0 and self.novel.chapters[chId].oldType != 0:
                    continue

                chapterCount += 1

                if self.novel.chapters[chId].chLevel == 0:
                    headingPrefix = '## '

                else:
                    headingPrefix = '# '

                # Get chapter titles.

                if self.novel.chapters[chId].title:
                    chapterTitles.append('- ' + self.novel.chapters[chId].title)
                    sceneHeading = '\n' + headingPrefix + self.novel.chapters[chId].title + '\n'
                    sceneTitles.append(sceneHeading)

                # Get chapter descriptions.

                if self.novel.chapters[chId].desc:
                    chapterDescriptions.append('\n' + headingPrefix + self.novel.chapters[chId].title + '\n')
                    chapterDescriptions.append(convert_from_yw(self.novel.chapters[chId].desc))

                for scId in self.novel.chapters[chId].srtScenes:

                    if not (self.novel.scenes[scId].isUnused or self.novel.scenes[scId].isNotesScene or self.novel.scenes[scId].isTodoScene):
                        sceneCount += 1

                        # Get scene titles.

                        if self.novel.scenes[scId].title:
                            sceneTitles.append('- ' + self.novel.scenes[scId].title)

                        # Get scene descriptions.

                        if self.novel.scenes[scId].desc:
                            sceneDescriptions.append(sceneHeading)
                            sceneDescriptions.append(convert_from_yw(self.novel.scenes[scId].desc))

                        # Get scene contents.

                        if self.novel.scenes[scId].sceneContent:
                            sceneContents.append(sceneHeading)
                            sceneContents.append(convert_from_yw(self.novel.scenes[scId].sceneContent))

                        sceneHeading = self.SCENE_DIVIDER

                        # Get scene word count.

                        if self.novel.scenes[scId].wordCount:
                            wordCount += self.novel.scenes[scId].wordCount

            self.statusBar.config(text=str(chapterCount) + ' chapters, ' +
                                  str(sceneCount) + ' scenes, ' + str(wordCount) + ' words')

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

    def show_text(self, text):

        if self.novel is not None:
            self.textBox['state'] = 'normal'
            self.textBox.delete('1.0', END)
            self.textBox.insert('1.0', text)
            self.textBox['state'] = 'disabled'

    def close_file(self):
        self.novel = None
        self.textBox['state'] = 'normal'
        self.textBox.delete('1.0', END)
        self.titleBar.config(text='')
        self.statusBar.config(text='')
        self.pathBar.config(text='')

    def run(self):
        menubar = tk.Menu(self.mainWindow)
        menuF = tk.Menu(menubar, title='my title', tearoff=0)

        menubar.add_cascade(label='Project', menu=menuF)

        menuF.add_command(label='Open..', command=lambda: self.open_file())
        menuF.add_command(label='Properties', command=lambda: self.show_text(self.properties))
        menuF.add_command(label='Close', command=lambda: self.close_file())
        menuF.add_command(label='Exit', command=self.mainWindow.quit)

        menuC = tk.Menu(menubar, title='my title', tearoff=0)

        menubar.add_cascade(label='Chapters', menu=menuC)  # Top Line

        menuC.add_command(label='Chapter titles', command=lambda: self.show_text(self.chapterTitles))
        menuC.add_command(label='Chapter descriptions', command=lambda: self.show_text(self.chapterDescriptions))

        menuS = tk.Menu(menubar, title='my title', tearoff=0)

        menubar.add_cascade(label='Scenes', menu=menuS)  # Top Line

        menuS.add_command(label='Scene titles', command=lambda: self.show_text(self.sceneTitles))
        menuS.add_command(label='Scene descriptions', command=lambda: self.show_text(self.sceneDescriptions))
        menuS.add_command(label='Scene contents', command=lambda: self.show_text(self.sceneContents))

        self.mainWindow.config(menu=menubar)

        self.titleBar = tk.Label(self.mainWindow,  text='')
        self.titleBar.pack(expand=False, anchor='w')

        self.textBox = scrolledtext.ScrolledText(self.mainWindow,  height=30,
                                                 width=60, undo=True, autoseparators=True, maxundo=-1, spacing1=0, spacing2=3, wrap='word')
        self.textBox.pack(expand=True, fill='both', padx=4, pady=4)

        self.statusBar = tk.Label(self.mainWindow,  text='')
        self.statusBar.pack(expand=False, anchor='w')
        self.pathBar = tk.Label(self.mainWindow,  text='')
        self.pathBar.pack(expand=False, anchor='w')

        if self.fileName:
            self.open_file(self.fileName)

        self.mainWindow.mainloop()
