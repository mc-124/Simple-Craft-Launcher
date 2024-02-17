from .net import requests 
import subprocess
import json
from shutil import rmtree
from os import makedirs
from shutil import rmtree
from .java import get_java_info
from . import TMPDIR
from .utils import id_16b,get_file_hash,strip
from .error import MinecraftVersionError,CompatibilityError
from .minecraft import get_mc_info
from .mods import ModInfo
from os.path import join
from zipfile36 import ZipFile,ZipInfo,ZipExtFile
from  typing_extensions import Literal
import pyxdelta

class InstallOptifine:
    def __init__(self,mcdir:str,version:str,optifine_installer:str) -> None:
        self.mcdir = mcdir
        self.version = version
        self.installer = optifine_installer
        self.killed = False
        self.process = 0.0
        "进度"
        self.mode = None
        "安装方式"

    def install_optifabric(self) -> None:
        "安装 方式:fabric"
        ...

    def start(self) -> None:
        '''
        启动安装
        '''
        with open(join(self.mcdir,'versions',self.version),encoding='utf-8') as jsonf:
            json_data = json.load(jsonf)
        info = get_mc_info(json_data)
        if 'optifine' in info.loader:
            raise FileExistsError("Optifine已安装")
        if 'quilt' in info.loader:
            raise CompatibilityError("Quilt与Optifine不兼容")
        if 'fabric' in info.loader:
            self.mode = 3
            self.install_optifabric()
        else: # 原版/forge/liteloader
            offo = ZipFile(self.installer,'r')
            try:
                for file in offo.filelist: # 判断是新版还是旧版optifine
                    file:ZipInfo
                    if file.filename.startswith('patch/notch/com'):
                        self.mode = 1
                        break
                else:
                    self.mode = 2
            finally:
                offo.close()
            if self.mode == 1: # 新版
                self.install_new()
            else:
                self.install_old()

    def install_new(self) -> None:
        "安装 方式:新版optifine"
        with open(join(self.mcdir,'versions',self.version,'%s.jar'%self.version),'r',encoding='utf-8') as f:
            jsondata = json.load(f)
        try:
            jarfo = ZipFile(join(self.mcdir,'versions',self.version,'%s.jar'%self.version),'r')
            offo = ZipFile(self.installer)
            xdelta_files = []
            md5_files = []
            for off in offo.filelist:
                off:ZipInfo
                if off.filename.startswith('patch/notch/'):
                    if off.filename.endswith('.xdelta'):
                        xdelta_files.append(off)
                    elif off.filename.endswith('.md5'):
                        ...

        finally:
            try:
                jarfo.close()
            except:
                pass
            try:
                offo.close()
            except:
                pass

    

    def install_old(self) -> None:
        "安装 方式:旧版optifine"
