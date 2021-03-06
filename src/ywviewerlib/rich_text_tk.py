#!/usr/bin/env python3
""""Provide a tkinter Rich Text box class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-viewer
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import scrolledtext
from tkinter import font as tkFont


class RichTextTk(scrolledtext.ScrolledText):
    """A text box applying formatting.
    Kudos to Bryan Oakley
    https://stackoverflow.com/questions/63099026/fomatted-text-in-tkinter
    """
    H1_TAG = 'h1'
    H2_TAG = 'h2'
    H3_TAG = 'h3'
    ITALIC_TAG = 'italic'
    BOLD_TAG = 'bold'
    CENTER_TAG = 'center'
    BULLET_TAG = 'bullet'

    H1_SIZE = 1.2
    H2_SIZE = 1.1
    H3_SIZE = 1.0
    H1_SPACING = 2
    H2_SPACING = 2
    H3_SPACING = 1.5
    CENTER_SPACING = 1.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        defaultFont = tkFont.nametofont(self.cget('font'))

        em = defaultFont.measure('m')
        defaultSize = defaultFont.cget('size')
        boldFont = tkFont.Font(**defaultFont.configure())
        italicFont = tkFont.Font(**defaultFont.configure())
        h1Font = tkFont.Font(**defaultFont.configure())
        h2Font = tkFont.Font(**defaultFont.configure())
        h3Font = tkFont.Font(**defaultFont.configure())

        boldFont.configure(weight='bold')
        italicFont.configure(slant='italic')
        h1Font.configure(size=int(defaultSize * self.H1_SIZE), weight='bold')
        h2Font.configure(size=int(defaultSize * self.H2_SIZE), weight='bold')
        h3Font.configure(size=int(defaultSize * self.H3_SIZE), weight='bold')

        self.tag_configure(self.BOLD_TAG, font=boldFont)
        self.tag_configure(self.ITALIC_TAG, font=italicFont)
        self.tag_configure(self.H1_TAG, font=h1Font, spacing3=defaultSize,
                           justify='center', spacing1=defaultSize * self.H1_SPACING)
        self.tag_configure(self.H2_TAG, font=h2Font, spacing3=defaultSize,
                           justify='center', spacing1=defaultSize * self.H2_SPACING)
        self.tag_configure(self.H3_TAG, font=h3Font, spacing3=defaultSize, spacing1=defaultSize * self.H3_SPACING)
        self.tag_configure(self.CENTER_TAG, justify='center', spacing1=defaultSize * self.CENTER_SPACING)

        lmargin2 = em + defaultFont.measure('\u2022 ')
        self.tag_configure(self.BULLET_TAG, lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        self.insert(index, f'\u2022 {text}', self.BULLET_TAG)
