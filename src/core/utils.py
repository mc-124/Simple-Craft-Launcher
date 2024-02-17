from xml.etree import ElementTree
from typing import List,Dict,Union,Tuple
from typing_extensions import Literal
from zipfile import ZipFile,ZIP_DEFLATED
from os import walk
from os.path import isfile,isdir,basename,join
from datetime import datetime,timedelta
from time import timezone,localtime,altzone
from io import TextIOWrapper
from locale import getdefaultlocale
from hashlib import new as hashlib_new
from time import time_ns
from random import shuffle,seed
import sys
import subprocess
import platform

class Any(object):pass
_m = platform.machine().lower()

_X64 = ('x64','x86_64','amd64','intel64')
_X86 = ('x86','i686')
_ARM64 = ('arm64','aarch64')
_ARM32 = ('arm32','aarch32')

X64 = 'x64'
X86 = 'x86'
A64 = 'arm64'
A32 = 'arm32'
O64 = '?64'
O32 = '?32'
UNKNOWN_ARCH = ''

if platform.machine().lower() in _X64:
    ARCH = X64
elif platform.machine().lower() in _X86:
    ARCH = X86
elif platform.machine().lower() in _ARM64:
    ARCH = A64
elif platform.machine().lower() in _ARM32:
    ARCH = A32
elif '64' in platform.machine():
    ARCH = O64
elif ('32' in platform.machine()) or ('86' in platform.machine()):
    ARCH = O32
else:
    ARCH = UNKNOWN_ARCH
ARCH:Literal['x64','x86','arm64','arm32','?64','?32','']


def read_popen(cmd:Union[str,list],shell:bool=False) -> subprocess.Popen:
    'subprocess.Popen.stdout'
    return subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=shell)

def xml_to_dict(xml_string) -> dict:
    "把xml转换为dict"
    def recursive_parse(element):
        if len(element) == 0:return element.text
        element_dict = {}
        for child in element:
            if child.tag not in element_dict:element_dict[child.tag] = recursive_parse(child)
            else:
                if type(element_dict[child.tag]) is list:element_dict[child.tag].append(recursive_parse(child))
                else:element_dict[child.tag] = [element_dict[child.tag],recursive_parse(child)]
        return element_dict
    root = ElementTree.fromstring(xml_string)
    return {root.tag:recursive_parse(root)}

def ISO8601_to_datetime(iso8601) -> datetime:
    "把mojang喜欢用的iso8601转换为datetime"
    return datetime.strptime(((datetime.strptime(iso8601,"%Y-%m-%dT%H:%M:%S%z"))+timedelta(hours=((-timezone if (localtime().tm_isdst == 0) else-altzone)/3600))).strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')

def change_process_priority(pid:int,priority:int) -> None:
    '''
    更改进程优先级(only win32)
    :pid: 进程PID
    :priority: 优先级
    0:空闲
    1:较低
    2:正常
    3:较高
    4:高
    5:实时
    '''
    prioritys = [64,16384,32,32768,128,256]
    subprocess.call('wmic process where processid=%d CALL setpriority %d'%(pid,prioritys[priority]))

def get_system_version() -> str:
    if sys.platform == 'win32': # WIN32
        ver = platform.version().split('.') # '10.0.19041' -> '10.0'
        if len(ver) > 1:
            return '%s.%s'%(ver[0],ver[1])
        else:
            return ver
    else: # UNIX
        ver = platform.release().split('-')[0] # '4.4.0-19041-Microsoft' -> '4.4.0'
        return ver
    
def uuid_is_steve(uuid:str) -> bool:
    '''
    UUID是史蒂夫皮肤
    :uuid: minecraft uuid
    * 注：此函数是从PCL2搬过来的
    '''
    if len(uuid) != 32:
        return True
    a = int(uuid[7],16)
    b = int(uuid[15],16)
    c = int(uuid[23],16)
    d = int(uuid[31],16)
    return False if (a ^ b ^ c ^ d) % 2 else True

class Match:
    def __init__(self,val:object) -> None:
        self.__v = val
        self.__i = 0

    def __call__(self,val:object) -> bool:
        ret = self.__v == val
        self.__i += int(ret)
        return ret
    
    def Else(self) -> bool:
        return not self.__i
    
def get_os_language() -> str:
    '获取系统语言 如zh_CN'
    return getdefaultlocale()[0]

def get_os_encode() -> str:
    '获取系统编码 如cp936'
    return getdefaultlocale()[1]

def strip(string:str) -> str:
    "清理字符串中无用的空格与换行"
    string = string.replace('\r','')
    while True:
        if string.startswith(' '):
            string = string[1:]
        else:
            break
    while True:
        if string.endswith(' '):
            string = string[:-1]
        else:
            break
    return string.strip()

class OptionsParser:
    def __init__(self,data:str) -> None:
        self.lines = data.split('\n')

    def _get_line_key_val(self,line:str) -> Union[Tuple[str,str],None]:
        "获取单行的键值对"
        if ':' in line:
            key = strip(line[:line.index(':')])
            val = strip(line[line.index(':')+1:])
            return key,val
        else:
            return None

    def _get_keys_vals(self) -> Dict[str,str]:
        "获取整个文件的键值对"
        return_ = {}
        for line in self.lines:
            ln = self._get_line_key_val(line)
            if ln:
                return_[ln[0]] = ln[1]
        return return_
    
    def __contains__(self,item:str) -> bool: # in
        return item in self._get_keys_vals()

    def get(self,key:str,not_found_ok:bool=True) -> Union[str,None]:
        '''
        获取键对应值
        :key: 键
        :not_found_ok: 在找不到键时不引发错误
        '''
        kv = self._get_keys_vals()
        if key in kv:
            return kv[key]
        if not_found_ok:
            return
        raise KeyError(key)
        
    def set(self,key:str,new_val:str) -> None:
        '''
        设置键的新值
        :key: 键
        :new_val: 新值
        '''
        kv = self._get_keys_vals()
        if key in kv: # 存在这个键
            for index,line in enumerate(self.lines):
                ln = self._get_line_key_val(line)
                if ln:
                    self.lines[index] = '{key}:{value}'.format(key=key,value=new_val)
        else:
            self.lines.append('{key}:{value}'.format(key=key,value=new_val))

    def write_string(self) -> str:
        "把数据写入字符串"
        data = '\n'.join(self.lines)
        if not data.endswith('\n'):
            data += '\n'
        return data
    
    def write(self,fp:TextIOWrapper) -> None:
        "把数据写入文件"
        fp.write(self.write_string())

def check_version_range(version:Tuple[int,int,int],version_range:str) -> None:
    """
    检查版本号元组是否在范围
    :version: 版本号元组
    :version_range: 字符串版本号范围
    """
    start_char,start_version_str,end_version_str,end_char = version_range[0],version_range[1:-1],version_range[-1],None
    if ',' in version_range:
        end_version_str = version_range.split(',')[1]
    start_version = tuple(map(int,start_version_str.split('.')))
    end_version = tuple(map(int,end_version_str.split('.'))) if end_version_str else None
    if start_char == '[':
        if version >= start_version:
            return True
    elif start_char == '(':
        if version > start_version:
            return True
    if end_char == ']':
        if version < end_version:
            return True
    elif end_char == ')':
        if version <= end_version:
            return True
    return False

def is_java_format(string:str) -> bool:
    return string.startswith('${') and string.endswith('}')

def get_file_hash(file:str,algorithm:Literal['md5','sha1','sha224','sha256','sha384','sha512']='md5'):
    """
    获取文件哈希值
    :file: 文件路径
    :algorithm: 哈希类型
    """
    hasher = hashlib_new(algorithm)
    with open(file,'rb') as file:
        for chunk in iter(lambda:file.read(4096),b''):
            hasher.update(chunk)
    return hasher

def replaces(*obj_:Union[str,Tuple[str,str,Union[None,int]]]) -> str:
    "一次replace多个字符串"
    string:str = obj_[0]
    obj:Tuple[Tuple[str,str],...] = obj_[1:]
    for t in obj:
        if len(t) == 3:
            string = string.replace(t[0],t[1],t[2])
        else:
            string = string.replace(t[0],t[1])
    else:
        return string
    
def id_16b() -> str:
    strings = [s for s in 'qwertyuiopasdfghjklzxcvbnm7418529630'*32]
    shuffle(strings)
    return ''.join(strings)[:16]