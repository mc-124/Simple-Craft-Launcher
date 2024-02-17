from tkinter import Tk,Frame as Fr
from tkinter.ttk import Style
from . import page_download,page_launch,page_more,page_settings
#from .page_launch import (
#    PageLaunch
#)
from utils import log
from init import init

if __name__ != "__main__":
    from . import (Style)
    from .controls import test#MainWindow
else:
    import ui.page_launch as page_launch,ui.page_download as page_download,ui.page_settings as page_settings,ui.page_more as page_more
    from controls import MainWindow

def MainApplication() -> None:
    import core
    import utils
    try:
        import secrecy
        core.CURSEFORGE_API_KEY = secrecy.BTAAAAMgAAAE8AAAByAAAAbAAAAGwAAAB6()
        utils.translation = secrecy.translation_func
    except:
        pass
    init()

    #log.info('main','start')
    #def window_close() -> None:
    #    app.destroy()
    #    print('app-destroy')
    #app = MainWindow(False,index_frame=page_launch,title="Simple-Craft-Launcher",geometry='800x500',window_close_command=window_close)
    #app.add_frame(
    #    
    #)
    #app.start()
    test()

if __name__ == "__main__":
    MainApplication()