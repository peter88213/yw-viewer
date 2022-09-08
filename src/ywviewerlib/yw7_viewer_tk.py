""""Provide a tkinter GUI framework for yWriter file viewing.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import tkinter as tk
from pywriter.ui.main_tk import MainTk
from pywriter.ui.set_icon_tk import *
from ywviewerlib.file_viewer import FileViewer


class Yw7ViewerTk(MainTk):
    """A tkinter GUI class for yWriter file viewing.
    
    Public methods:
        disable_menu() -- disable menu entries when no project is open.
        enable_menu() -- enable menu entries when a project is open.
        open_project(fileName) -- create a yWriter project instance and read the file. 
        close_project() -- close the yWriter project without saving and reset the user interface.

    Public instance variables:
        treeWindow -- tk window for the project tree.

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
        self.kwargs = kwargs
        super().__init__(title, **kwargs)
        set_icon(self.root, icon='vLogo32')
        self.viewerWindow = tk.Frame(self.mainWindow)
        self.viewerWindow.pack(expand=True, fill='both')
        self._fv = FileViewer(self)

    def _build_main_menu(self):
        """Add main menu entries.
        
        Extends the superclass template method. 
        """
        super()._build_main_menu()
        self._quickViewMenu = tk.Menu(self.mainMenu, title='my title', tearoff=0)
        self.mainMenu.add_cascade(label='Quick view', underline=0, menu=self._quickViewMenu)
        self.mainMenu.entryconfig('Quick view', state='disabled')
        self._quickViewMenu.add_command(label='Project description', underline=0,
                                        command=lambda: self._fv.view_text(self._fv.prjDescription))
        self._quickViewMenu.add_command(label='Chapter titles', underline=8,
                                        command=lambda: self._fv.view_text(self._fv.chapterTitles))
        self._quickViewMenu.add_command(label='Chapter descriptions', underline=0,
                                       command=lambda: self._fv.view_text(self._fv.chapterDescriptions))
        self._quickViewMenu.add_command(label='Scene titles', underline=7,
                                        command=lambda: self._fv.view_text(self._fv.sceneTitles))
        self._quickViewMenu.add_command(label='Scene descriptions', underline=6,
                                       command=lambda: self._fv.view_text(self._fv.sceneDescriptions))
        self._quickViewMenu.add_command(label='Scene contents', underline=7,
                                        command=lambda: self._fv.view_text(self._fv.sceneContents))
        self._quickViewMenu.insert_separator(1)
        self._quickViewMenu.insert_separator(4)

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Extends the superclass method.      
        """
        super().disable_menu()
        self.mainMenu.entryconfig('Quick view', state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Extends the superclass method.
        """
        super().enable_menu()
        self.mainMenu.entryconfig('Quick view', state='normal')

    def open_project(self, fileName):
        """Create a yWriter project instance and prepare the content for viewing.

        Positional arguments:
            fileName -- str: project file path.
            
        Display the total numbers of chapters, scenes and words.
        Return True on success, otherwise return False.
        Extends the superclass method.
        """
        if not super().open_project(fileName):
            return False

        self.show_status(self._fv.build_views())
        self._fv.view_text(self._fv.prjDescription)
        return True

    def close_project(self, event=None):
        """Clear the text box.
        
        Extends the superclass method.
        """
        super().close_project()
        self._fv.reset_view()
