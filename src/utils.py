from datetime import datetime
from os import makedirs,getenv,rename,getcwd,system as os_system
from os.path import isfile,abspath,exists,dirname,join,isdir
import subprocess
from hashlib import md5
from json import loads,dumps,load,dump
from types import FunctionType as Function
from platform import system,machine
from typing import Union,List,Dict,NoReturn
from psutil import virtual_memory
import _version
from _tkinter import TclError
from core.utils import ARCH,strip,replaces
from resources import LOGDIR
from base64 import b64encode,b64decode
import sys

# ensure_ascii=False

# explorer.exe /select,<fp>

__SELF__:str = sys.argv[0]
NoneType = type(None)
class Any(object):pass
class Types(object):pass
class PlatformError(Exception):pass
argv_lock:bool = True
'''
随意改变此变量的值可能引起正式版数据被损坏
'''
def is_bin(fp:str) -> bool:
    bs = b'\x00\x01\x03\x04\x14\x18\x10\x12\x1f\x08\x1a'
    with open(fp,'rb') as f:
        for b in f.read(32768):
            if b in bs:return True
        else:return False
def null_func(*a,**k) -> None:return
try:
    import secrecy
    if (
        (
            __SELF__.endswith('.py') or
            __SELF__.endswith('.pyc') or 
            __SELF__.endswith('.pyz') or
            __SELF__.endswith('.pyzw') or
            not is_bin(__SELF__)
        ) and argv_lock):raise
    DEV = False
except:
    DEV = True

translation = null_func

#region DEV
if __name__ != '__main__':
    import secrecy
    CURSEFORGE_API_KEY = ...
#endregion

if sys.platform == 'win32':
    from ctypes import windll,c_uint
    def info_sound():
        "播放提示音"
        windll.user32.MessageBeep(c_uint(-1))
    def error_sound():
        "播放错误音"
        windll.user32.MessageBeep(c_uint(0x00000010))
elif sys.platform == 'linux':
    def info_sound():
        "播放提示音"
        os_system('echo -en "\x07"')
    error_sound = info_sound # Linux不知道要调用什么玩意去发出声响……
    "播放错误音"
elif sys.platform == 'darwin':
    def info_sound():
        "播放提示音"
        os_system('osascript -e "beep 1"')
    def error_sound():
        "播放错误音"
        os_system('osascript -e "beep 2"')
else:
    info_sound = null_func
    error_sound = null_func

def get_memory() -> object:
    memory = virtual_memory()
    return memory

def remove_self() -> NoReturn:
    "退出并自我删除"
    if sys.platform == 'win32':
        subprocess.Popen('timeout /t 2 /nobreak&del "%s"'%__SELF__)
        sys.exit(0)
    else:
        subprocess.Popen('sleep 2 ; rm "%s"'%__SELF__)
        sys.exit(0)

STR_NONE = Union[str,NoneType]

# FILE_NAME                   VERSION   AUTHOR
# forge-install-bootstrapper  0.2.0     bangbang93
# authlib-injector            1.2.4     yushijinhun
# 7-zip_windows-x86           23.01     7-zip
# 7-zip_windows-arm64         23.01     7-zip
# 7-zip_linux-amd64           23.01     7-zip
# webviewer                   1.0.0     mc-124
# convert(PILLOW)             1.0.0     mc-124

# CONFIG
LOG_NUM = 5
#endregion

if DEV:
    _LOG = 'debug'
else:
    _LOG = 'log'

class log:
    LOGDIR = LOGDIR
    LOG1 = join(LOGDIR,'log-1.log')
    ENCODE = 'utf-8'

    INFO = 'Info'
    WARN = "Warn"
    ERROR = "Error"

    def _init() -> None:
        makedirs(LOGDIR,exist_ok=True)
        for i in range(LOG_NUM-1,0,-1):
            if isfile(f'{LOGDIR}\\{_LOG}-{i}.log'):
                rename(f'{LOGDIR}\\{_LOG}-{i}.log',f'{LOGDIR}\\{_LOG}-{i+1}.log')
        with open(log.LOG1,'w',encoding=log.ENCODE) as fp:
            fp.write(
'''\
Simple-Craft-Launcher 
version: {version}
version-type: {versionType}
time: {time}
platform: {platform}
arch: {arch}
python-version: {python_version}
'''.format(
    version=_version.__version__,
    versionType=_version.__versionType__,
    time=datetime.now(),
    platform=sys.platform,
    arch=ARCH,
    python_version=sys.version
)
            )

    def info(mod:str,*logs:Any) -> None:
        log._write(mod,log.INFO,*logs)
    
    def warn(mod:str,*logs:Any) -> None:
        log._write(mod,log.WARN,*logs)
    
    def error(mod:str,*logs:Any) -> None:
        log._write(mod,log.ERROR,*logs)

    def program_stoping(exitcode:int=0,remself:bool=False) -> NoReturn:
        if remself:
            log._write('MAIN',log.INFO,*['Stopping!!'])
            remove_self()
        else:
            log._write('MAIN',log.INFO,*['Stopping!!'])
            sys.exit(exitcode)
    
    def program_crash(exitcode:int=1) -> NoReturn:
        log._write('MAIN',log.INFO,*['Program crash!!'])
        sys.exit(exitcode)
    
    def _write(mod:str,state:str,*logs:Any) -> None:
        time = str(datetime.now())
        log_list = []
        for l in logs:log_list.append(str(l))
        log_data = ' '.join(log_list)
        with open(log.LOG1,'a',encoding=log.ENCODE) as fp:
            fp.write(
                "[{time}][{mod}][{state}] {log_data}".format(
                    time=time,
                    mod=mod,
                    state=state,
                    log_data=log_data
                )
            )

def strip_start(_str:str) -> str:
    string = _str.replace('\r','')
    while True:
        if string.startswith(' '):
            string = string[1:]
        else:
            break
    return string

def strip_end(_str:str) -> str:
    string = _str.replace('\r','')
    while True:
        if string.endswith(' '):
            string = string[:-1]
        else:
            break
    return string

if sys.platform == 'win32':    
    class Scanner:
        """
        ## 检测系统中的fractureiser病毒
        ##### 此代码由CurseForge的DetectionTool反编译后GPT4.0转换得来
        --------
        ##### 调用方法
        ```python
        Scanner().Scan()
        ```
        --------
        ##### 返回值
        ```python
        {
            "DetectedFiles":[],    # 扫描到的病毒文件
            "FoundInPath":False    # 在Path内发现病毒
            "FoundInStartUp":False # 在开始菜单发现病毒
        }
        or
        None    # 系统不支持扫描
        ```
        """
        def __init__(self):
            self._suspiousEdgeFiles = [".ref","client.jar","lib.dll","libWebGL64.jar","run.bat"]
            self._localAppData = getenv('LOCALAPPDATA')
            self._malwareAppDataPath = self._localAppData + "\\Microsoft Edge"
            self._malwareStartupFilePath = getenv('APPDATA') + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\run.bat"

        def Scan(self):
            scanResults = {'DetectedFiles':[],'FoundInPath':False,'FoundInStartUp':False}
            detectedFiles = self.CheckFiles()
            if detectedFiles:
                scanResults['DetectedFiles'] = detectedFiles
                scanResults['FoundInPath'] = True
            startupStatus = self.CheckStartup()
            if startupStatus:
                scanResults['FoundInStartUp'] = True
                scanResults['DetectedFiles'].append(self._malwareStartupFilePath)
            return scanResults

        def CheckFiles(self):
            detectedFiles = []
            if exists(self._malwareAppDataPath):
                for file in self._suspiousEdgeFiles:
                    suspiciousFilePath = self._malwareAppDataPath+"\\"+file
                    if exists(suspiciousFilePath):
                        detectedFiles.append(suspiciousFilePath)
            return detectedFiles

        def CheckStartup(self):
            return exists(self._malwareStartupFilePath)
else:
    class Scanner:
        def __init__(self) -> None:
            self.return_ = None
        def Scan(self) -> None:
            return self.return_

# NOTE 下面这两个函数纯属闲的
def py_error_parse(traceback:str) -> dict:
    "解析python引发的错误"
    def _split_list(lst:List[str]) -> list:
        out:List[List[str]] = []
        for _l in lst:
            l = strip(_l)
            if l.startswith('File "'):
                out.append([l])
            else:
                out[-1].append(l)
        return out
    traceback = strip(traceback)
    if not traceback.startswith('Traceback'):
        raise ValueError("traceback format is incorrect")
    files = []
    lines:List[List[str]] = _split_list(traceback.split('\n')[1:-1])
    errinfo = traceback.split('\n')[-1]
    for fc in lines:
        s = fc[0].split('", ')
        fp = s[0][6:]
        s2 = s[1][5:].split(', ')
        ln = int(s2[0])
        in_ = s2[1][3:] if len(s2) > 1 else None
        c = strip('\n'.join(fc[1:]))
        files.append({"file":fp,"line":ln,"in":in_,"code":c})
    et = errinfo[:errinfo.index(': ')]
    ei = errinfo[errinfo.index(': ')+2:]
    return {'type':et,'info':ei,'files':files}

def traceback_format(traceback_:str) -> str:
    "把python错误格式化"
    def _func(s:str) -> str:
        if '\n' in s:
            r = ''
            sn = s.split('\n')
            for l in sn:
                r += '\n      %s'%l
            return r
        else:
            return s
    traceback = py_error_parse(traceback_)
    errline = '\n   at {in} {file}[{line}]: {err}'
    errtext = 'SCL ERROR. {type}: {info}'.format(type=traceback['type'],info=traceback['info'])
    for ef in traceback['files']:
        ef:dict
        errtext += errline.format(**{'in':ef['in'],'file':ef['file'],'line':ef['line'],'err':_func(ef['code'])})
    return errtext

def attrib_addH(fp:str) -> None:
    if sys.platform == 'win32':
        os_system('attrib +h "%s"'%fp)

def attrib_remH(fp:str) -> None:
    if sys.platform == 'win32':
        os_system('attrib -h "%s"'%fp)

def ini_b64encode(data:Union[bytes,str]) -> str:
    return replaces((b64encode(data if type(data) == bytes else data.decode('utf-8'))).decode('utf-8'),('+','.b0'),('/','.b1'),('=','.b2'))

def ini_b64decode(data:str) -> bytes:
    return b64decode(replaces(data,('.b0','+'),('.b1','/'),('.b2','=')))



#def test():
#    print(traceback_format(error_info))



if __name__ == "__main__": # test
    ...