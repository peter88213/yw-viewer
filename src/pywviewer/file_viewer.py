#!/usr/bin/env python3
""""Provide a class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
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

    def __init__(self, fileName='', **kwargs):
        if fileName:
            self.fileName = fileName

        elif kwargs['yw_last_open']:
            self.fileName = kwargs['yw_last_open']

        else:
            self.fileName = ''

        self.kwargs = kwargs
        self.mainWindow = tk.Tk()
        # change width height
        self.init_dir = os.path.dirname(fileName)
        self.novel = None

    def open_file(self, fileName=''):

        if not fileName:
            fileName = filedialog.askopenfilename(filetypes=[('yWriter 7 project', '.yw7')],
                                                  defaultextension='.yw7', initialdir=self.init_dir)

        if fileName:
            self.kwargs['yw_last_open'] = fileName
            self.novel = Yw7File(fileName)
            self.novel.read()

            if self.novel.title:
                text = self.novel.title

            else:
                text = 'Untitled yWriter project'

            self.mainWindow.title(text)

            self.show_project_description()

    def show_project_description(self):

        if self.novel is not None:

            if self.novel.desc:
                text = self.novel.desc

            else:
                text = '(No project description available)'

            self.textBox.delete('1.0', END)
            # remove the previous content
            self.textBox.insert('1.0', text)
            # add new data from file to text box

    def show_chapter_titles(self):

        if self.novel is not None:
            titles = []

            for chId in self.novel.srtChapters:

                if self.novel.chapters[chId].title:
                    titles.append(self.novel.chapters[chId].title)

            text = '\n'.join(titles)

            if not text:
                text = '(No chapter titles available)'

            self.textBox.delete('1.0', END)
            # remove the previous content
            self.textBox.insert('1.0', text)
            # add new data from file to text box

    def show_chapter_descriptions(self):

        if self.novel is not None:
            descriptions = []

            for chId in self.novel.srtChapters:

                if self.novel.chapters[chId].desc:
                    descriptions.append(self.novel.chapters[chId].desc)

            text = '\n'.join(descriptions)

            if not text:
                text = '(No chapter descriptions available)'

            self.textBox.delete('1.0', END)
            # remove the previous content
            self.textBox.insert('1.0', text)
            # add new data from file to text box

    def show_scene_titles(self):

        if self.novel is not None:
            titles = []

            for chId in self.novel.srtChapters:

                for scId in self.novel.chapters[chId].srtScenes:

                    if self.novel.scenes[scId].title:
                        titles.append(self.novel.scenes[scId].title)

            text = '\n'.join(titles)

            if not text:
                text = '(No scene titles available)'

            self.textBox.delete('1.0', END)
            # remove the previous content
            self.textBox.insert('1.0', text)
            # add new data from file to text box

    def show_scene_descriptions(self):

        if self.novel is not None:
            descriptions = []

            for chId in self.novel.srtChapters:

                for scId in self.novel.chapters[chId].srtScenes:

                    if self.novel.scenes[scId].desc:
                        descriptions.append(self.novel.scenes[scId].desc)

            text = '\n'.join(descriptions)

            if not text:
                text = '(No scene descriptions available)'

            self.textBox.delete('1.0', END)
            # remove the previous content
            self.textBox.insert('1.0', text)
            # add new data from file to text box

    def show_scene_contents(self):

        if self.novel is not None:
            contents = []

            for chId in self.novel.srtChapters:

                for scId in self.novel.chapters[chId].srtScenes:

                    if self.novel.scenes[scId].sceneContent:
                        contents.append(self.novel.scenes[scId].sceneContent)

            text = '\n'.join(contents)

            if not text:
                text = '(No scene contents available)'

            self.textBox.delete('1.0', END)
            # remove the previous content
            self.textBox.insert('1.0', text)
            # add new data from file to text box

    def close_file(self):
        self.novel = None

        self.textBox.delete('1.0', END)
        # remove the content from text widget

        self.mainWindow.title('')
        # remove the title of GUI

    def run(self):
        menubar = tk.Menu(self.mainWindow)
        menuF = tk.Menu(menubar, title='my title', tearoff=0)

        menubar.add_cascade(label='Project', menu=menuF)

        menuF.add_command(label='Open..', command=lambda: self.open_file())
        menuF.add_command(label='Description', command=lambda: self.show_project_description())
        menuF.add_command(label='Close', command=lambda: self.close_file())
        menuF.add_command(label='Exit', command=self.mainWindow.quit)

        menuC = tk.Menu(menubar, title='my title', tearoff=0)

        menubar.add_cascade(label='Chapters', menu=menuC)  # Top Line

        menuC.add_command(label='Chapter titles', command=lambda: self.show_chapter_titles())
        menuC.add_command(label='Chapter descriptions', command=lambda: self.show_chapter_descriptions())

        menuS = tk.Menu(menubar, title='my title', tearoff=0)

        menubar.add_cascade(label='Scenes', menu=menuS)  # Top Line

        menuS.add_command(label='Scene titles', command=lambda: self.show_scene_titles())
        menuS.add_command(label='Scene descriptions', command=lambda: self.show_scene_descriptions())
        menuS.add_command(label='Scene contents', command=lambda: self.show_scene_contents())

        self.mainWindow.config(menu=menubar)
        self.textBox = scrolledtext.ScrolledText(self.mainWindow,  height=30,
                                                 width=60, undo=True, autoseparators=True, maxundo=-1, spacing1=10, spacing2=3, wrap='word')
        self.textBox.pack(expand=True, fill='both')

        if self.fileName:
            self.open_file(self.fileName)

        self.mainWindow.mainloop()


if __name__ == '__main__':
    viewer = FileViewer()
    viewer.run()
