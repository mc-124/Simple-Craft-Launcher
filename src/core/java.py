from os.path import isfile,isdir,abspath
from .net import requests
from .utils import OptionsParser,replaces
from typing import List,Dict,Union,Tuple
import subprocess
from multiprocessing import Process,Manager,Queue
from multiprocessing.managers import ListProxy
from psutil import disk_partitions
from os import listdir,walk,sep,getenv
from os.path import isdir,isfile,join,basename,dirname
from typing_extensions import Literal
from traceback import format_exc
import sys

def get_java_info(fp:str) -> Dict[str,object]:
    '''
    获取java信息
    :fp: java的可执行文件
    '''
    java_root_dir = dirname(dirname(fp))
    release_file = join(java_root_dir,'release')
    with open(release_file,'r',encoding='utf-8') as relf:
        data = relf.read()
        op = OptionsParser(data)
        java_version = replaces(op.get('JAVA_VERSION',False),(' ',''),('"',''),('_','.'))
        java_arch = replaces(op.get('OS_ARCH',False),(' ',''),('"',''))
        java_version = java_version[2:] if java_version.startswith('1.') else java_version
        java_ver_tup:Tuple[int,int,int] = tuple([int(i) for i in java_version.split('.')])
    java_type = ''
    for d in listdir(java_root_dir):
        if isdir(join(java_root_dir,d)):
            if d.lower() not in ('bin','lib','legal'):
                java_type = 'jdk'
                break
    else:
        java_type = 'jre'
    return {
        "path":java_root_dir,
        "version":java_ver_tup,
        "arch":java_arch,
        "type":java_type
    }

def search_java(java_roots:ListProxy,catch:Queue) -> None:
    '''
    全盘搜索java 需要通过multiprocessing启动
    :java_roots: multiprocessing.Manager.list()
    :catch: multiprocessing.Queue()
    '''
    def _search(path:str):
        dir_names = ( # 搜索关键词
            'java','bin','jre','jvm','client','jdk','program','env','world','i386',
            'mc','soft','roaming','craft','users','net','game','server','version',
            'mojang','oracle','data','x86','x64','x86_64','amd64','arm64','432',
            'arm32','ms','microsoft','runtime','eclipse','launch','aarch','path',
            'mod','forge','fabric','qulit','laby','hmcl','multi','baka','bugjump',
            'pcl','scl','download','optifine','hotspot','corretto','4297127d64ec6',
            'local',"azul","zulu","ibm",'ext','1.','pack','folder','163','i686',
            'documents','win32','linux','osx','lib','cleanroom',
            "环境","软件","游戏","世界","服务端","客户端","运行","文件夹","高清",
            "前置","整合","官方","官启","启动","网易","应用","原版","模组","程序",
        )
        last_fp = None
        try:
            for dn,sds,sfs in walk(path):
                last_fp = dn
                for n in dir_names:
                    if n in basename(dn).lower() and '$' not in n:
                        for fn in sfs:
                            fp = join(dn,fn)
                            last_fp = fp
                            if basename(fp).lower() == ('java.exe' if sys.platform == 'win32' else 'java'):
                                java_roots.append(get_java_info(fp))
                            else:
                                continue
                    else:
                        continue
        except Exception:
            error = {
                "error-info":format_exc(),
                'last-parse':last_fp
            }
            catch.put(error)
            raise
    for disk in [d.device for d in disk_partitions()] if disk_partitions() else ['/']:
        try:
            _search(disk)
        except:
            break