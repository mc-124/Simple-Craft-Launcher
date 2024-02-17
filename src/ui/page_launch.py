from tkinter.ttk import (
    Frame,
    Button
)
from .language import lang
from .controls import MainWindow

class PageLaunch(Frame):
    def __init__(self,parent:MainWindow) -> None:
        super().__init__(parent)
        self.launch_button = Button(self,width=22,text="test button",style="LaunchGameButton.TButton")
        self.launch_button.place(x=518,y=280)

