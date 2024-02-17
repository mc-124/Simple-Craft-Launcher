from os import makedirs
from core.net import requests
from traceback import format_exc as error
from utils import (
    LOGDIR,
    log
)
from tkinter import messagebox
from resources import (
    restore_dir
)

def init() -> None:
    log._init()
    log.info('INIT','正在初始化程序')
    ... # TODO 未做完