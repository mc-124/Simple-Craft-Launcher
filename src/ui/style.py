'tkinter样式'
from typing import Tuple

class Font(object):
    bold = 'bold'
    "粗体"
    italic = 'italic'
    "斜体"
    underline = 'underline'
    "下划线"
    overstrike = 'overstrike'
    "删除线"

class Style(object):
    def __init__(self,
        background:str=None,
        activebackground:str=None,
        foreground:str=None,
        activeforeground:str=None,
        disabledforeground:str=None,
        highlightbackground:str=None,
        cursor:str=None,
        bd:int=0,
        font:Tuple[str,int,str]=None,
        selectforeground:str=None,
        insertbackground:str=None,
        width:int=None,
        height:int=None,
    ) -> None:
        self.background = background
        self.activebackground = activebackground
        self.foreground = foreground
        self.activeforeground = activeforeground
        self.disabledforeground = disabledforeground
        self.highlightbackground = highlightbackground
        self.cursor = cursor
        self.bd = bd
        self.font = font
        self.selectforeground = selectforeground
        self.insertbackground = insertbackground
        self.width = width
        self.height = height

    def __call__(self) -> dict:
        kw = {}
        if self.background:
            kw['background'] = self.background
        if self.activebackground:
            kw['activebackground'] = self.activebackground
        if self.foreground:
            kw['foreground'] = self.foreground
        if self.activeforeground:
            kw['activeforeground'] = self.activeforeground
        if self.disabledforeground:
            kw['disabledforeground'] = self.disabledforeground
        if self.highlightbackground:
            kw['highlightbackground'] = self.highlightbackground
        if self.cursor:
            kw['cursor'] = self.cursor
        if self.bd != None:
            kw['bd'] = self.bd
        if self.font:
            kw['font'] = self.font
        if self.selectforeground:
            kw['selectforeground'] = self.selectforeground
        if self.insertbackground:
            kw['insertbackground'] = self.insertbackground
        if self.width:
            kw['width'] = self.width
        if self.height:
            kw['height'] = self.height
        return kw
    
    def __str__(self) -> str:
        return "<tkStyle>"
    
if __name__ == "__main__":
    from tkinter import Tk,Button,Text
    tk = Tk()
    s = Style(
        '#BBBBBB',
        "#FFFF00",
        '#FFFFFF',
        None,
        width=20,
        height=10,
        font=()
    )
    b = Button(tk,**s())
    b.pack()
    tk.mainloop()