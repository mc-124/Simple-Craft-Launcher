from .net import requests
from . import TMPDIR
from os.path import isfile,basename,join
from os import listdir
from .error import JSONTypeError
from .utils import ISO8601_to_datetime
from typing_extensions import Literal
from typing import Any, Dict,Union
from json import load

class MinecraftInfo:
    def __init__(s) -> None:
        s.loader = {}
        s.mc_version = ''
        s.mc_id = ''
        s.jre = ''
        s.jre_type = ''
        s.mc_type = ''
        s.update_time = ''
        s.release_time = ''

def get_mc_info(json_data:dict) -> MinecraftInfo:
    '''
    获取mc信息
    :json_data: mc的json数据
    '''
    forge = fabric = optifine = version = version_id = version_type = quilt = jre_version = jre_type = liteloader = None
    for lib in json_data['libraries']:
        lib:Dict[str,Union[str,dict,list]]
        if lib['name'].startswith('optifine:OptiFine:'):
            optifine = lib['name'].split(':')[-1]
        if lib['name'].startswith('net.minecraftforge:forge:'):
            _str = lib['name'].split(':')[-1].split('-')
            version = _str[0]
            forge = _str[1]
        if lib['name'].startswith('net.fabricmc:fabric-loader:'):
            fabric = lib['name'].split(':')[-1]
        if lib['name'].startswith('net.fabricmc:intermediary:'):
            version = lib['name']
        if lib['name'].startswith('org.quiltmc:quilt-loader:'):
            quilt = lib['name'].split(':')[-1]
        if lib['name'].startswith('com.mumfrey:liteloader:'):
            liteloader = lib['name'].split(':')[-1]
    jre_type = json_data['javaVersion']['component']
    jre_version = json_data['javaVersion']['majorVersion']
    if not version:
        if 'clientVersion' in json_data:
            version = json_data['clientVersion']
        else:
            version = json_data['id']
    version_id = json_data['id']
    version_type = json_data['type']
    update_time = json_data['time']
    release_time = json_data['releaseTime']
    info = MinecraftInfo()
    if forge:
        info.loader['forge'] = forge
    if fabric:
        info.loader['fabric'] = fabric
    if quilt:
        info.loader['quilt'] = quilt
    if optifine:
        info.loader['optifine'] = optifine
    if liteloader:
        info.loader['liteloader'] = liteloader
    info.mc_version = version
    info.mc_id = version_id
    info.jre = jre_version
    info.jre_type = jre_type
    info.mc_type = version_type
    info.update_time = update_time
    info.release_time = release_time
    return info