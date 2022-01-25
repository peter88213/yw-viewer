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

from pywriter.ui.root_tk import RootTk
from pywviewer.yw7_file_view import Yw7FileView


class Yw7ViewerTk(RootTk):
    """A tkinter GUI class for yWriter file viewing.

    Show titles, descriptions, and contents in a text box.
    """

    def __init__(self, title, **kwargs):
        """Put a text box to the GUI main window.
        Extend the superclass constructor.
        """
        super().__init__(title, **kwargs)
        self.textBox = scrolledtext.ScrolledText(self.mainWindow,  height=30,
                                                 width=60, undo=True, autoseparators=True, maxundo=-1, spacing1=0, spacing2=3, wrap='word')
        self.textBox.pack(expand=True, fill='both', padx=4, pady=4)

    def extend_menu(self):
        """Add main menu entries.
        Override the superclass template method. 
        """
        self.menuQ = tk.Menu(self.menubar, title='my title', tearoff=0)
        self.menubar.add_cascade(label='Quick view', menu=self.menuQ)  # Top Line
        self.menuQ.add_command(label='Project description', command=lambda: self.show_text(self.ywPrj.descView))
        self.menuQ.add_command(label='Chapter titles', command=lambda: self.show_text(self.ywPrj.chapterTitles))
        self.menuQ.add_command(label='Chapter descriptions',
                               command=lambda: self.show_text(self.ywPrj.chapterDescriptions))
        self.menuQ.add_command(label='Scene titles', command=lambda: self.show_text(self.ywPrj.sceneTitles))
        self.menuQ.add_command(label='Scene descriptions',
                               command=lambda: self.show_text(self.ywPrj.sceneDescriptions))
        self.menuQ.add_command(label='Scene contents', command=lambda: self.show_text(self.ywPrj.sceneContents))
        self.menuQ.insert_separator(1)
        self.menuQ.insert_separator(4)

    def disable_menu(self):
        """Disable menu entries when no project is open.
        Extend the superclass method.      
        """
        super().disable_menu()
        self.menubar.entryconfig('Quick view', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        Extend the superclass method.
        """
        super().enable_menu()
        self.menubar.entryconfig('Quick view', state='normal')

    def show_text(self, text):
        """Load text into the text box.
        Disable text editing.
        """
        self.textBox['state'] = 'normal'
        self.textBox.delete('1.0', END)

        if text:
            self.textBox.insert('1.0', text)

        self.textBox['state'] = 'disabled'

    def instantiate_project(self, fileName):
        """Create an object that represents the project file.
        Override the superclass template method. 
        """
        self.ywPrj = Yw7FileView(fileName)

    def open_project(self, fileName):
        """Show the project description after reading the file.
        Return True if sucessful, otherwise return False.
        Extend the superclass method.
        """
        if super().open_project(fileName):
            self.show_text(self.ywPrj.descView)
            return True

        return False

    def close_project(self):
        """Clear the text box.
        Extend the superclass method.
        """
        super().close_project()
        self.textBox['state'] = 'normal'
        self.textBox.delete('1.0', END)
        self.textBox['state'] = 'disabled'
