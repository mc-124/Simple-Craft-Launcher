from .net import requests,DefaultHeaders,Response
from . import CURSEFORGE_API_KEY
from base64 import b64decode
from bs4 import BeautifulSoup
from error import ModNotFoundError,CFApiKeyNotFoundError
from os import makedirs
from zipfile36 import ZipFile,is_zipfile,ZipInfo,ZipExtFile
from typing import List,Dict,Union
from .utils import Match,OptionsParser,is_java_format
from hashlib import sha1
from typing_extensions import Literal
import io
import toml
import json

key:Response = requests.get('https://d.kstore.space/download/4904/SCL/cfapikey.txt')

CURSEFORGE_API_KEY = CURSEFORGE_API_KEY or key.text

MCMOD_SEARCH = "https://search.mcmod.cn/s"
MCMOD_SEARCH = "https://search.mcmod.cn/s"
CF_DOWNLOAD_URL = 'https://edge.forgecdn.net/files/{id4}/{id3}/{name}'

UNKNOWN_LOADER = ''
FORGE_LOADER = 'forge'
FABRIC_LOADER = 'fabric'
NEOFORGE_LOADER = 'neoforge'

PARAMS_MCMOD = {
    "key":'',
    'filter':"1",
    'mold':'0',
    'page':'1'
}
DEFAULT_HEADERS = DefaultHeaders.browser_headers
CURSEFORGE_API_URL = 'https://api.curseforge.com'

HEADERS_CF = {
    'Accept':'application/json',
    'x-api-key':CURSEFORGE_API_KEY
}

CF_LOADER_TYPE = {
    0:'any',
    1:'forge',
  # 2: unkonwn
    3:'liteloader',
    4:'fabric',
    5:'quilt'
}

CF_RELEASE_TYPE = {
    1:'release',
    2:'beta',
    3:'alpha'
}

MCMOD_MOD_TYPE = {
    1:  "t",    # 科技
    2:  'm',    # 魔法
    3:  'v',    # 冒险
    4:  'f',    # 农业
    5:  'd',    # 装饰
    7:  'l',    # 支持
    21  :'r',   # 魔改
    23  :'ut',  # 实用
    24  :'h',   # 辅助
}

def mcmod_search(name:str,page_index:int=1) -> dict:
    'v1'
    output = {}
    p2 = PARAMS_MCMOD
    p2['key'] = name
    p2['page'] = str(page_index)
    response = requests.get(MCMOD_SEARCH,p2)
    response.raise_for_status()
    soup = BeautifulSoup(response.text,'html.parser')
    div_tag = soup.find('div',class_='search-result-list')
    if not div_tag:
        raise ModNotFoundError("找不到Mod")
    info = soup.find('p', class_='info')
    info_text = ''
    for tag in info:
        if tag.text.replace('\n','').replace(' ',''):
            info_text = tag.text.replace('\n','')
            #print("信息：",info_text)
    length = ''
    length_text = info_text[4:]
    for l in length_text:
        if l == ' ':
            break
        else:
            length += l
    length = int(length)
    use_time = info_text[-15:-3].split(':')[-1]
    pages_text = (info_text.split('，')[-1].split('。')[0])[3:]
    pages = ''
    for t in pages_text:
        if t == ' ':
            break
        else:
            pages += t
    pages = int(pages)
    output['search-use-time'] = use_time
    output['search-length'] = length
    output['page-num'] = pages
    output['data'] = []
    div_2x = div_tag.find_all('div',class_='result-item')
    for div_2 in div_2x:
        Data = {}
        div_3 = div_2.find('div',class_='head')
        a_1 = div_3.find_all('a')
        url = ''
        for a in a_1:
            if a.get('class'):
                #print('类型：',''.join(a.get('class')))
                Data['type'] = ''.join(a.get('class'))
            else:
                #print("名称：",a.text.replace('\n',''))
                Data['name'] = a.text.replace('\n','')
                url = ''.join(a.get('href'))
                #print("MCMOD网址：",url)
                Data['mcmod'] = url
        div_desc = div_2.find('div',class_='body')
        #print("描述：",div_desc.text)
        Data['desc'] = div_desc.text
        r = requests.get(url,headers=DEFAULT_HEADERS)
        r.raise_for_status()
        soup2 = BeautifulSoup(r.text,'html.parser')
        ul = soup2.find('ul',class_='common-link-icon-frame common-link-icon-frame-style-3')
        lis = ul.find_all('li')
        curseforge = ''
        modrinth = ''
        github = ''
        mcbbs = ''
        for li in lis:
            lia = li.find('a')
            if 'CurseForge' in lia.get('data-original-title'): # data-original-title="Modrinth"
                curseforge_b64 = ''.join(lia.get('href'))
                if curseforge_b64.endswith('/'):
                    curseforge_b64 = curseforge_b64[-1].split('/')[-1]
                else:
                    curseforge_b64 = curseforge_b64.split('/')[-1]
                curseforge = b64decode(curseforge_b64).decode('utf-8')
            elif 'Modrinth' in lia.get('data-original-title'):
                modrinth_b64 = ''.join(lia.get('href'))
                if modrinth_b64.endswith('/'):
                    modrinth_b64 = modrinth_b64[-1].split('/')[-1]
                else:
                    modrinth_b64 = modrinth_b64.split('/')[-1]
                modrinth = b64decode(modrinth_b64).decode('utf-8')
            elif 'Github' in lia.get('data-original-title'):
                github_b64 = ''.join(lia.get('href'))
                if github_b64.endswith('/'):
                    github_b64 = github_b64[-1].split('/')[-1]
                else:
                    github_b64 = github_b64.split('/')[-1]
                github = b64decode(github_b64).decode('utf-8')
            elif 'MCBBS' in lia.get('data-original-title'):
                mcbbs_b64 = ''.join(lia.get('href'))
                if mcbbs_b64.endswith('/'):
                    mcbbs_b64 = mcbbs_b64[-1].split('/')[-1]
                else:
                    mcbbs_b64 = mcbbs_b64.split('/')[-1]
                mcbbs = b64decode(mcbbs_b64).decode('utf-8')
        #print("Github网址：",github)
        #print("MCBBS网址：",mcbbs)
        #print('CurseForge网址：',curseforge)
        #print('Modrinth网址：',modrinth)
        Data['github'] = github
        Data['mcmod'] = mcbbs
        Data['curseforge'] = curseforge
        Data['modrinth'] = modrinth
        output['data'] = Data
    return output

#region test
from json import dumps,dump
def _format_json_print(d:object) -> None:
    print(dumps(d,ensure_ascii=False,indent=4))

def _write(d:object) -> None:
    with open('output4.json','w',encoding='utf-8') as f:
        dump(d,f,ensure_ascii=False,indent=4)
#endregion

def get_slug(url:str) -> str:
    if url.endswith('/'):
        url = url[:-1]
    return url.split('/')[-1]

class CurseForge:
    def get_mc_gameId() -> str:
        'v1'
        if not CURSEFORGE_API_KEY:
            raise CFApiKeyNotFoundError('没有CurseForgeAPI key')
        response = requests.get(CURSEFORGE_API_URL+'/v1/games',headers=HEADERS_CF)
        response.raise_for_status()
        code = None
        for d in response.json['data']:
            if d['slug'] == 'minecraft':
                code = d['id']
                break
        if not code:
            raise FileNotFoundError("找不到mc的id")
        return code
        
    def slug_search(slug:str,mcid:int) -> None:
        'v1' # test slug: jei
        if not CURSEFORGE_API_KEY:
            raise CFApiKeyNotFoundError('没有CurseForgeAPI key')
        params = {
            'gameId':str(mcid),
            'slug':slug
        }
        response = requests.get(CURSEFORGE_API_URL+'/v1/mods/search',headers=HEADERS_CF,params=params)
        response.raise_for_status()
        return CurseForge.parse_mod(response.json)
        
    def parse_mod(json:dict) -> dict:
        json = json['data'][0]
        forge = []
        fabric = []
        liteloader = []
        quilt = []
        unknown_loader = []
        versions = []
        files_json = json['latestFilesIndexes']
        for file in files_json:
            version = file['gameVersion']
            name = file['filename']
            Type = CurseForge.get_version_type(file['releaseType'])
            url = CurseForge.get_file_url(file['fileId'],name)
            loader = 'unknown' if 'modLoader' not in file else CurseForge.get_loader_type(file['modLoader'])
            dic = {'version':version,'name':name,'type':Type,'url':url}
            if loader == 'forge':
                forge.append(dic)
            elif loader == 'fabric':
                fabric.append(dic)
            elif loader == 'quilt':
                quilt.append(dic)
            elif loader == 'liteloader':
                liteloader.append(dic)
            else:
                unknown_loader.append(dic)
            if version not in versions:
                versions.append(version)
        return {
            "id":json['id'],
            "name":json['name'],
            "url":json['links']['websiteUrl'],
            "summary":json['summary'],
            "download-count":json['downloadCount'],
            'icon':json['logo']['url'],
            'files':{
                'forge':forge,
                'fabric':fabric,
                'liteloader':liteloader,
                'quilt':quilt,
                'unknown':unknown_loader
            },
            'versions':versions
        }            
    
    def get_loader_type(t:int) -> str:
        if t in CF_LOADER_TYPE:
            return CF_LOADER_TYPE[t]
        else:
            return 'unknown'
    
    def get_version_type(t:int) -> str:
        if t in CF_RELEASE_TYPE:
            return CF_RELEASE_TYPE[t]
        else:
            return 'unknown'
        
    def get_file_url(id:int,fn:str) -> str:
        id = str(id)
        id4,id3 = id[:4],id[4:]
        return CF_DOWNLOAD_URL.format(id4=id4,id3=id3,name=fn)

# pack.mcmeta: JSON
# mcmod.info: JSON
# fabric.mod.json: JSON
# manifest.mf: kvp

class _ModInfo:
    def __init__(self,
                 icon:ZipInfo,
                 icon_path:str,
                 name:str,
                 url:str,
                 issues:str,
                 description:str,
                 authors:List[str],
                 id_:str,
                 mcversion:str,
                 loader:str,
                 ) -> None:
        self.icon:ZipInfo =         icon
        self.icon_path:str =        icon_path
        self.name:str =             name
        self.url:str =              url
        self.issues:str =           issues
        self.description:str =      description
        self.authors:List[str] =    authors
        self.id:str =               id_
        self.mcversion:str =        mcversion
        self.loader:str =           loader
        

class ModInfo:
    '获取mod的信息'
    def __init__(self,zfp:ZipFile) -> None:
        '''
        :zfp: ZipFile对象
        '''
        self.zf = zfp

    def __enter__(self,filepath:str) -> None:
        '''
        :filepath: 文件路径
        '''
        self.zf = ZipFile(filepath,'r')

    def __exit__(self,_0,_1,_2) -> None:
        self.zf.close()
    
    def get_modinfo(self) -> object:
        "获取mod的类型"
        mod_icon = None
        mod_name = ''
        mod_icon_path = ''
        mod_url = ''
        mod_issues = ''
        mod_description = ''
        mod_version = ''
        mod_id = ''
        mod_mcversion = ''
        mod_loader:Literal['forge','fabric','neoforge'] = ''
        # 暂时无法识别liteloader和quilt
        mod_author = []
        #mod_side:Literal['CLIENT','SERVER'] = ''
        for file in self.zf.filelist:
            file:ZipInfo
            if file.filename.lower() == 'meta-inf/mods.toml': # forge / neoforge 新版
                with self.zf.open(file) as f:
                    f:ZipExtFile
                    mods_toml = toml.loads(f.read().decode('utf-8'))
                if "mods" in mods_toml:
                    mods:List[Dict[str,str]] = mods_toml['mods']
                    if 'logoFile' in mods:
                        mod_icon_path = mod_icon_path or mods['logoFile']
                    if 'authors' in mods:
                        mod_author = mod_author or ([mods['authors']] if type(mods['authors']) == str else mods['authors'])
                    if 'modId' in mods:
                        mod_id = mod_id or mods['modId']
                    if 'displayName' in mods:
                        mod_name = mod_name or mods['displayName']
                    if 'displayURL' in mods:
                        mod_url = mod_url or mods['displayURL']
                    if "description" in mods:
                        mod_description = mod_description or mods["description"]
                if 'dependencies' in mods_toml and mod_id:
                    if mod_id in mods_toml['dependencies']:
                        dependencies:Dict[str,str] = mods_toml['dependencies'][mod_id]
                        if 'modId' in dependencies:
                            mod_loader = mod_loader or dependencies['modId']
                        else: 
                            mod_loader = mod_loader or 'forge'
            if file.filename.lower() == 'mcmod.info': # forge
                mod_loader = mod_loader or 'forge'
                with self.zf.open(file) as f:
                    f:ZipExtFile
                    info:Dict[str,Union[str,List[Union[str,Dict[str,object]]]]] = json.loads(f.read().decode('utf-8'))
                if 'modid' in info:
                    if not is_java_format(info['modid']):
                        mod_id = mod_id or info['modid']
                if 'version' in info:
                    if not is_java_format(info['version']):
                        mod_version = mod_version or info['version']
                if "description" in info:
                    if not is_java_format(info['description']):
                        mod_description = mod_description or info["description"]
                if 'mcversion' in info:
                    if not is_java_format(info['mcversion']):
                        mod_mcversion = mod_mcversion or info['mcversion']
                if 'url' in info:
                    if not is_java_format(info['url']):
                        mod_url = mod_url or info['url']
                if 'authorList' in info:
                    if not is_java_format(info['authorList']):
                        mod_author = mod_author or info['authorList']
                if 'logoFile' in info:
                    if not is_java_format(info['logoFile']):
                        mod_icon_path = mod_icon_path or info['logoFile']
            if file.filename.lower() == 'fabric.mod.json': # fabric
                mod_loader = mod_loader or 'fabric'
                with self.zf.open(file) as f:
                    modjson:Dict[str,Union[str,int,dict,list]] = json.loads(f.read().decode('utf-8'))
                if 'id' in modjson:
                    mod_id = modjson['id']
                if 'version' in modjson:
                    mod_version = modjson['version']
                if 'icon' in modjson:
                    mod_icon_path = modjson['icon']
                if 'description' in modjson:
                    mod_description = modjson['description']
                if 'name' in modjson:
                    mod_name = modjson['name']
                if 'authors' in modjson:
                    for author in modjson['authors']:
                        mod_author.append(author['name'])
                if 'contack' in modjson:
                    if 'sources' in modjson['contack']:
                        mod_url = modjson['contack']['sources']
                    if 'issues' in modjson['contack']:
                        mod_issues = modjson['contack']['issues']
                if 'depends' in modjson:
                    if 'minecraft' in modjson:
                        mod_mcversion = modjson['depends']
                break
        for file in self.zf.filelist:
            if file.filename == mod_icon_path:
                mod_icon = file
        return _ModInfo(
            icon=mod_icon,
            icon_path=mod_icon_path,
            name=mod_name,
            url=mod_url,
            issues=mod_issues,
            description=mod_description,
            authors=mod_author,
            id_=mod_id,
            mcversion=mod_mcversion,
            loader=mod_loader
        )
    
    def write_icon(self,fileobj:_ModInfo,fp:io.BufferedWriter) -> str:
        """
        把图标写入文件 返回文件格式
        :fileobj: get_modinfo返回的对象
        :fp: wb文件对象
        """
        with self.zf.open(fileobj.icon) as f:
            f:ZipExtFile
            fp.write(f.read())
        return fileobj.icon_path.split('.')[-1].upper()
    
    def get_icon_sha1(self,fileobj:_ModInfo) -> str:
        '''
        获取图标的SHA1
        :fileobj: get_modinfo返回的对象
        '''
        with self.zf.open(fileobj.icon) as f:
            f:ZipExtFile
            data = f.read()
        return sha1(data).hexdigest()