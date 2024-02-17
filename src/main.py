# coding: utf-8
r'''
```
   _____ ________                           __             
  / ___// ____/ /   ____ ___  ______  _____/ /_  ___  _____
  \__ \/ /   / /   / __ `/ / / / __ \/ ___/ __ \/ _ \/ ___/
 ___/ / /___/ /___/ /_/ / /_/ / / / / /__/ / / /  __/ /    
/____/\____/_____/\__,_/\__,_/_/ /_/\___/_/ /_/\___/_/   
                                Copyright (C) mc-124                                                                                                                                                                             
```

## ![scl_icon](https://mc-124.github.io/mcl-scl/assets/scl-16.png) Simple-Craft-Launcher
开源、免费的Minecraft启动器

---------
## MIT License

Copyright (c) 2023 mc-124

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import sys
import os 
import datetime
import platform
from typing import NoReturn
from traceback import format_exc

#region [EXIT_CODE]
# 0: 正常退出
# 1: 未知错误
# 1xxx: 启动时崩溃
# 1000: 缺失tkinter
# 1001: 无图形界面
# 1002: 缺失模块
# 1003: 文件损坏
# 1004: 无法导入multiprocessing
# 1006: python版本不对
# 1111: 未知
#endregion

def _main_crash(e:object,traceback:str,string:str,ver:tuple,vt:str,code:int=1) -> NoReturn:
    try:
        os.system('echo \x07')
        with open('Crash.log','w') as f:
            f.write('''\
SCL Crash
program-version: %s
program-version-type: %s
python: %s
python-platform: %s
python-module-path: %s
system-type: %s
system-platform: %s
crash-time: %s
__file__: %s
self: %s
error: %s
error-info: \n%s\n%s\
'''%(ver,vt,sys.version,platform.architecture(),sys.path,sys.platform,platform.platform(),datetime.datetime.now(),sys.argv[0],__file__,e,traceback,string))
        if sys.platform == 'win32':
            os.system('explorer /select,Crash.log')
    except:
        pass
    finally:
        sys.exit(code)

def __main__() -> None:
    win32_3582_490_1 = (os.getenv('SYSTEMROOT')).lower()+'\\temp\\3582-490';win32_3582_490_2 = (os.getenv('TEMP') or os.getenv('TMP')).lower()+'\\3582-490'
    try:from info import __versionType__,__version__
    except ModuleNotFoundError as e:
        _main_crash(e,format_exc(),'module "project_info" not found.',(-1,-1,-1),'UNKNOWN',1002)
    if sys.version_info.major != 3 or sys.version_info.minor != 7:
        _main_crash
    if os.path.abspath(__file__).lower().startswith(win32_3582_490_1) or os.path.abspath(__file__).lower().startswith(win32_3582_490_2):
        _main_crash('SCL has been infected by the computer virus Neshta.','SCL has been infected by the computer virus Neshta and cannot continue to operate.','SCL has been infected by the computer virus Neshta and cannot continue to operate.',__version__,__versionType__,1003)
    try:from multiprocessing import Process;p=Process();p.start();p.kill()
    except Exception as e:_main_crash(e,format_exc(),"Cannot import multiprocessing",__version__,__versionType__,1004)
    try:from tkinter import Tk
    except Exception as e:_main_crash(e,format_exc(),"Module \"tkinter\" not found.",__version__,__versionType__,1000)
    try:Tk().destroy()
    except Exception as e:_main_crash(e,format_exc(),"Cannot display.",__version__,__versionType__,1001)
    try:
        from ui import MainApplication
        MainApplication()
    except Exception as e:
        _main_crash(e,format_exc(),str(e),__version__,__versionType__,1111)
    
    
if __name__ == "__main__":
    __main__()