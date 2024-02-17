from os import makedirs,getenv
from os.path import abspath,dirname,isfile,getsize,join,sep
from typing import List,Dict
from core.utils import get_file_hash
from base64 import b85decode,b85encode
import _resources
import sys
import _version
from send2trash import send2trash

#region env
_LOCAL = (getenv('APPDATA')if sys.platform=='win32'else getenv('HOME')) or '~'
_TMPDIR = (getenv('TEMP') or getenv('TMP') or getenv('TMPDIR') or ('TEMPDIR')) or sep+'tmp'
_CWD = dirname(sys.argv[0])
#endregion

#region path
SCL_DIR = join(_CWD,'SCL')
"当前目录"
NAME = 'scl'if _version.__versionType__!='dev'else'scl-dev'
DATA_DIR = join(_LOCAL,'.%s'%NAME)
"数据目录"
USERS_DIR = join(DATA_DIR,'users')
"用户配置信息目录"
CONFIG_DIR = join(DATA_DIR,'config')
"配置文件目录"
PLUGINS_DIR = join(DATA_DIR,"plugins")
"插件目录"
ASSETS_DIR = join(DATA_DIR,'assets')
"assets目录（*.png,*.json）"
BIN_DIR = join(DATA_DIR,'bin')
"bin目录（*.jar）"
LANG_DIR = join(DATA_DIR,'languages')
"语言文件目录（*.lang）"
CACHE_DIR = join(DATA_DIR,'cache')
"缓存文件目录（图片）"
TEMPDIR = join(_TMPDIR,NAME.upper())
"临时文件目录"
TEMP_DOWNLOAD = join(TEMPDIR,'download')
"下载时产生的临时文件目录"
TEMP_INSTALL = join(TEMPDIR,'install')
"安装时产生的临时文件目录"
LOGDIR = join(SCL_DIR,'logs')
"日志目录"
IMAGE_CACHE = join(CACHE_DIR,'images')
"图片缓存"

# windows
# msedge: %SYSTEMDRIVE%\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
# chrome: %SYSTEMDRIVE%\Program Files (x86)\Google\Chrome\Application\chrome.exe
# linux
# msedge: /opt/microsoft/msedge/msedge
# chrome: /opt/google/chrome/chrome
# osx
# msedge: /Application/Microsoft Edge.app
# chrome: /Application/Google Chrome.app


#endregion

#region bin
JAR_AUTHLIB_INJECTOR_PATH = join(BIN_DIR,'authlib_injector-1.2.4.jar')
JAR_FORGE_INSTALL_BOOTSTRAPPER_PATH = join(BIN_DIR,'forge_install_bootstrapper-0.2.0.jar')
JAR_OPTIFINE_INSTALLER_PATH = join(BIN_DIR,'optifine_installer-0.1.0.jar')
JAR_JAVA_LAUNCH_WRAPPER = join(BIN_DIR,"java_launch_wrapper-1.3.3.jar")
#endregion

#region default-constant
LOGNUM = 10

#endregion

#region url
# 自己的服务器禁不起折腾……只能用github.io
SCL_PLUGINS = 'https://mc-124.github.io/scl-server/plugins.ini'
SCL_VERSIONS = 'https://mc-124.github.io/scl-server/versions.ini'
SCL_BEHAVIOR = 'https://mc-124.github.io/scl-server/behavior.ini'
#endregion


_get_sha1 = lambda fp:get_file_hash(fp,'sha1')

def restore_dir(obj:List[Dict[str,str]],outdir:str) -> None:
    makedirs(outdir,exist_ok=True)
    outdir = abspath(outdir)
    for dic in obj:
        def _w():
            makedirs(dirname(fp),exist_ok=True)
            with open(fp,'wb') as fw:
                fw.write(b85decode(dic['data']))
        fp = dic['name'].replace('\x01',outdir)
        if isfile(fp):
            if _get_sha1(fp) != dic['sha1'] or getsize(fp) != int(dic['size'],16):
                _w()
            else:
                _w()
        else:
            _w()
    return
