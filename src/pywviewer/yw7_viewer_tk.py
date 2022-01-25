#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter file viewing.

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

from pywviewer.yw7_file_view import Yw7FileView


class Yw7ViewerTk():
    """A tkinter GUI class for yWriter file viewing.

    Show titles, descriptions, and contents in a text box.
    """

    def __init__(self, title, **kwargs):

        #--- Initialize the project related instance variables.

        self.kwargs = kwargs
        self.ywPrj = None

        #--- Configure the user interface.

        self.root = tk.Tk()
        self.root.title(title)

        self.menubar = tk.Menu(self.root)

        self.menuF = tk.Menu(self.menubar, title='my title', tearoff=0)
        self.menubar.add_cascade(label='Project', menu=self.menuF)
        self.menuF.add_command(label='Open Project...', command=lambda: self.open_project(''))
        self.menuF.add_command(label='Show Description', command=lambda: self.show_text(self.ywPrj.descView))
        self.menuF.add_command(label='Close Project', command=lambda: self.close_project())
        self.menuF.add_command(label='Exit', command=self.root.quit)

        self.menuC = tk.Menu(self.menubar, title='my title', tearoff=0)
        self.menubar.add_cascade(label='Chapters', menu=self.menuC)  # Top Line
        self.menuC.add_command(label='Chapter titles', command=lambda: self.show_text(self.ywPrj.chapterTitles))
        self.menuC.add_command(label='Chapter descriptions',
                               command=lambda: self.show_text(self.ywPrj.chapterDescriptions))

        self.menuS = tk.Menu(self.menubar, title='my title', tearoff=0)
        self.menubar.add_cascade(label='Scenes', menu=self.menuS)  # Top Line
        self.menuS.add_command(label='Scene titles', command=lambda: self.show_text(self.ywPrj.sceneTitles))
        self.menuS.add_command(label='Scene descriptions',
                               command=lambda: self.show_text(self.ywPrj.sceneDescriptions))
        self.menuS.add_command(label='Scene contents', command=lambda: self.show_text(self.ywPrj.sceneContents))

        self.root.config(menu=self.menubar)
        self.menuF.entryconfig('Show Description', state='disabled')
        self.menuF.entryconfig('Close Project', state='disabled')
        self.menubar.entryconfig('Chapters', state='disabled')
        self.menubar.entryconfig('Scenes', state='disabled')

        self.titleBar = tk.Label(self.root,  text='')
        self.titleBar.pack(expand=False, anchor='w')

        self.textBox = scrolledtext.ScrolledText(self.root,  height=30,
                                                 width=60, undo=True, autoseparators=True, maxundo=-1, spacing1=0, spacing2=3, wrap='word')
        self.textBox.pack(expand=True, fill='both', padx=4, pady=4)

        self.statusBar = tk.Label(self.root,  text='')
        self.statusBar.pack(expand=False, anchor='w')
        self.pathBar = tk.Label(self.root,  text='')
        self.pathBar.pack(expand=False, anchor='w')

    def start(self):
        """Start the Tk main loop."""
        self.root.mainloop()

    def open_project(self, fileName):
        initDir = os.path.dirname(fileName)

        if not initDir:
            initDir = './'

        if not fileName:
            fileName = filedialog.askopenfilename(filetypes=[('yWriter 7 project', '.yw7')],
                                                  defaultextension='.yw7', initialdir=initDir)

        if fileName:
            self.kwargs['yw_last_open'] = fileName
            self.pathBar.config(text=os.path.normpath(fileName))
            self.ywPrj = Yw7FileView(fileName)
            message = self.ywPrj.read()

            if message.startswith('ERROR'):
                self.close_project()
                self.statusBar.config(text=message)

            else:
                self.show_text(self.ywPrj.descView)
                self.titleBar.config(text=self.ywPrj.titleView)
                self.statusBar.config(text=self.ywPrj.statView)
                self.menuF.entryconfig('Show Description', state='normal')
                self.menuF.entryconfig('Close Project', state='normal')
                self.menubar.entryconfig('Chapters', state='normal')
                self.menubar.entryconfig('Scenes', state='normal')

    def show_text(self, text):
        self.textBox['state'] = 'normal'
        self.textBox.delete('1.0', END)

        if text:
            self.textBox.insert('1.0', text)

        self.textBox['state'] = 'disabled'

    def close_project(self):
        self.ywPrj = None
        self.textBox['state'] = 'normal'
        self.textBox.delete('1.0', END)
        self.textBox['state'] = 'disabled'
        self.titleBar.config(text='')
        self.statusBar.config(text='')
        self.pathBar.config(text='')
        self.menuF.entryconfig('Show Description', state='disabled')
        self.menuF.entryconfig('Close Project', state='disabled')
        self.menubar.entryconfig('Chapters', state='disabled')
        self.menubar.entryconfig('Scenes', state='disabled')
