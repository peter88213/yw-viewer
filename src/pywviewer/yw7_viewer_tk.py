#!/usr/bin/env python3
""""Provide a tkinter GUI class for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import tkinter as tk
from tkinter import scrolledtext
from tkinter import END
from tkinter import font as tkFont


from pywriter.ui.main_tk import MainTk
from pywviewer.rich_text_tk import RichTextTk
from pywviewer.yw7_file_view import Yw7FileView


class Yw7ViewerTk(MainTk):
    """A tkinter GUI class for yWriter file viewing.

    Show titles, descriptions, and contents in a text box.
    """

    def __init__(self, title, **kwargs):
        """Put a text box to the GUI main window.
        Extend the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self.textBox = RichTextTk(self.mainWindow,  height=20, width=60, undo=True, autoseparators=True, maxundo=-1,
                                  spacing1=10, spacing2=2, wrap='word', padx=40)
        self.textBox.pack(expand=True, fill='both', padx=4, pady=4)

    def extend_menu(self):
        """Add main menu entries.
        Override the superclass template method. 
        """
        self.quickViewMenu = tk.Menu(self.mainMenu, title='my title', tearoff=0)
        self.mainMenu.add_cascade(label='Quick view', menu=self.quickViewMenu)
        self.mainMenu.entryconfig('Quick view', state='disabled')
        self.quickViewMenu.add_command(label='Project description', command=lambda: self.show_text(self.ywPrj.descView))
        self.quickViewMenu.add_command(label='Chapter titles', command=lambda: self.show_text(self.ywPrj.chapterTitles))
        self.quickViewMenu.add_command(label='Chapter descriptions',
                                       command=lambda: self.show_text(self.ywPrj.chapterDescriptions))
        self.quickViewMenu.add_command(label='Scene titles', command=lambda: self.show_text(self.ywPrj.sceneTitles))
        self.quickViewMenu.add_command(label='Scene descriptions',
                                       command=lambda: self.show_text(self.ywPrj.sceneDescriptions))
        self.quickViewMenu.add_command(label='Scene contents', command=lambda: self.show_text(self.ywPrj.sceneContents))
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
        self.textBox.delete('1.0', END)

        for paragraph in text:
            self.textBox.insert(END, paragraph[0], paragraph[1])

        self.textBox['state'] = 'disabled'

    def open_project(self, fileName):
        """Create a yWriter project instance and read the file.
        Display project title, description and status.
        Return the file name.
        Extend the superclass method.
        """
        fileName = super().open_project(fileName)

        if not fileName:
            return ''

        self.ywPrj = Yw7FileView(fileName)
        message = self.ywPrj.read()

        if message.startswith('ERROR'):
            self.close_project()
            self.statusBar.config(text=message)
            return ''

        if self.ywPrj.title:
            titleView = self.ywPrj.title

        else:
            titleView = 'Untitled yWriter project'

        if self.ywPrj.author:
            authorView = self.ywPrj.author

        else:
            authorView = 'Unknown author'

        self.titleBar.config(text=titleView + ' by ' + authorView)
        self.show_text(self.ywPrj.descView)
        self.statusBar.config(text=self.ywPrj.statView)
        self.enable_menu()
        return fileName

    def close_project(self):
        """Clear the text box.
        Extend the superclass method.
        """
        super().close_project()
        self.textBox['state'] = 'normal'
        self.textBox.delete('1.0', END)
        self.textBox['state'] = 'disabled'
