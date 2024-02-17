'网络库'
from urllib import request,parse,error
from typing import Dict,List,Union,Tuple
from json import dumps,loads
from threading import Thread,get_ident
from http import client
from os import makedirs,remove
from os.path import join,abspath,isfile,getsize,isdir
from time import time
import sys
import ssl

SSLContext = ssl.SSLContext

from .utils import xml_to_dict,id_16b
from .error import *

HttpHeaders = Dict[str,str]
"请求头数据"
JSONData = Union[dict,list,str,int,None]
"JSON数据"
POSTData = str
"POST数据"
ParamsData = Union[Dict[str,object],List[object]]
"参数数据"
DataCoding = str
"数据编码"

KB = 1024
MB = 1024*KB
GB = 1024*MB

_UrlopenRet = client.HTTPResponse

disabled_ssl_context = ssl._create_unverified_context()

class DefaultHeaders:
    "默认请求头"
    if sys.platform == 'win32':
        browser_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}
    elif sys.platform == 'darwin':
        browser_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
    else: # linux
        browswe_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
    json_headers = {'Accept':'application/json'}

def urlformat(url:str,params:ParamsData=None) -> str:
    '''
    格式化URL
    :url: URL
    :params: 参数
    '''
    if not url.startswith('http'):
        url = 'http://'+url
    if not params:
        return url
    if '?' in url:
        if url.endswith('&') or url.endswith('?'):
            return url + parse.urlencode(params)
        else:
            return url +'&'+ parse.urlencode(params)
    else:
        return url +'?'+ parse.urlencode(params)

def ping_url(url:str) -> float:
    '''
    获取url对应服务器延迟
    :url: URL
    '''
    t1 = time()
    try:request.urlopen((url if 'http'in url else"http://"+url))
    except error.HTTPError:pass
    except error.URLError as e:raise RequestsError(e)
    t2 = time()
    return t2-t1

def get_chunks(total_size:int,block_size:int) -> List[tuple]:
    "分块"
    num_blocks = total_size // block_size
    blocks = []
    start = 0
    for i in range(num_blocks):
        end = start + block_size
        blocks.append((start,end))
        start = end
    if total_size % block_size != 0:
        blocks.append((start,total_size))
    return blocks

def split_list(lst:list,count:int) -> List[list]:
    "列表split"
    out = []
    index = 0
    while True:
        out.append([])
        try:
            for _ in range(count):
                out[-1].append(lst[index])
                index += 1
        except IndexError:
            break
    if not out[-1]:
        out.pop(-1)
    return out

class Response:
    def __init__(self,response_obj:_UrlopenRet=None,status:int=None,errmsg:str=None,code:str='utf-8') -> None:
        '''
        ## 响应
        '''
        self._obj = response_obj
        self._status = status
        self._errmsg = errmsg
        self._c = code
    
    @property
    def status_code(self) -> int:
        '状态码'
        if self._status:
            return self._status
        else:
            return self._obj.status
        
    def read(self,size:int=None) -> bytes:
        '读取二进制数据'
        return self._obj.read(size)
    
    def seek(self,offset:int=0) -> None:
        "移动指针"
        self._obj.seek(offset)
        
    @property
    def size(self) -> int:
        '大小'
        return self._obj.length

    def json(self) -> JSONData:
        '格式化json返回字典'
        return loads(self._obj.read().decode(self._c))
    
    @property
    def text(self) -> str:
        '返回文本'
        self._obj.seek(0)
        return self._obj.read().decode(self._c)
    
    @property
    def headers(self) -> HttpHeaders:
        '获取响应头'
        return dict(self._obj.headers.items())
    
    @property
    def url(self) -> str:
        '获取302后的url'
        return self._obj.url
    
    def raise_for_status(self) -> None:
        '状态码不对就报错'
        if self._status:
            if (self._status >= 400 and self._status < 600) or self._status < 200:
                raise StatusError(f"HTTP Error {self._status}: {self._errmsg}")
        else:
            status = self.status_code
            if (status >= 400 and status < 600) or status < 200:
                raise StatusError(f"HTTP Error {status}")
            
    if xml_to_dict:  
        def xml_dict(self) -> dict:
            '把xml数据转换为字典'
            return xml_to_dict(self.text)

class requests:
    def supports_range_requests(url:str,headers:HttpHeaders={},timeout:int=5) -> bool:
        "检测网站是否支持多线程下载"
        url = urlformat(url)
        response:_UrlopenRet = request.urlopen(request.Request(url,method='HEAD',headers=headers),timeout=timeout)
        return 'bytes' in response.headers.get('Accept-Ranges','')

    def get(url:str,headers:HttpHeaders=None,data:POSTData=None,json:JSONData=None,encoding:DataCoding='utf-8',params:ParamsData=None,timeout:Union[int,float]=5,try_count:int=1,Range:tuple=None,method:str='',context:ssl.SSLContext=disabled_ssl_context) -> Response:
        '''
        ### 发送GET/POST请求
        --------
        :url: URL
        :headers: 请求头
        :json: POST发送JSON数据
        :data: POST数据
        :encoding: 文本编码(为`"bytes"`时不进行编码)
        :params: 参数
        :timeout: 最大超时(秒)
        :try_count: 最大失败重试次数
        :Range: 获取数据段
        :method: 发送请求类型
        :context: SSL文本
        '''
        if not method:
            if data or json:
                method = 'POST'
            else:
                method = 'GET'
        if data and json:
            raise ValueError('"data" parameter and "json" cannot be used together.')
        url = urlformat(url,params)
        headers = headers if headers else {}
        if data or json:
            if data:
                _data:str = data
            else:
                _data:str = dumps(data,ensure_ascii=False)
            _data = _data.encode('utf-8')
        else:
            _data = None
        error_list:List[Exception] = []
        Request = request.Request(url=url,data=_data,headers=headers,method=method)
        if Range:
            if not requests.supports_range_requests():
                raise HostError("对方主机不支持分块下载")
        if Range and 'range' not in headers:
            Request.headers['Range'] = 'bytes={}-{}'.format(Range[0],Range[1])
        status:int = 0
        status_errmsg:Union[str,None] = None
        ok = False
        _response = None
        for _ in range(try_count):
            try:
                _response:_UrlopenRet = request.urlopen(Request,timeout=timeout,context=context)
            except error.HTTPError as e: # 状态码错误
                status = e.code
                status_errmsg = e.msg
                ok = True
                break
            except error.URLError as e:
                if '[Errno 11001]' in str(e): # 找不到主机
                    error_list.append(HostNotFoundError(f'Host not found: {url}'))
                elif 'timed out' in str(e): # 超时
                    error_list.append(HttpTimeOutError('Timed out'))
                else:
                    error_list.append(RequestsError(e))
            except Exception as e:
                error_list.append(RequestsError(e))
            else:
                ok = True
                break
        if len(error_list) == try_count:
            raise error_list[-1]
        elif ok:
            return Response(_response,code=encoding)
        else:
            return Response(None,status,status_errmsg,encoding)
        
    class Download:
        def __init__(self,url:str,save_path:str,headers:HttpHeaders=None,params:ParamsData=None,timeout:Union[int,float]=10,try_count:int=1,chunk_size:int=4*MB) -> None:
            '''
            ### 下载单个文件
            ------
            :url: URL
            :save_path: 保存路径
            :headers: 请求头
            :params: 参数
            :timeout: 最大超时(秒)
            :try_count: 最大失败重试次数
            :chunk_max_size: 每次写入大小
            '''
            self.downloaded_size = 0
            self._url = url
            self._path = save_path
            self._headers = headers
            self._params = params
            self._timeout = timeout
            self._try_count = try_count
            self._chunk_size = chunk_size
            self._thread = None
            self.ok = False
            self.start_noblock = self._thread_func
            "以阻塞主线程的方式启动下载"
        
        def _thread_func(self) -> None:
            "下载线程"
            if self.ok:
                raise RepeatTaskError("重复任务")
            url = format(self._url)
            response:Response = requests.get(url=url,headers=self._headers,params=self._params,timeout=self._timeout,try_count=self._try_count)
            self.size = response.size
            with open(self._path,'wb') as fp:
                while True:
                    chunk = response.read(self._chunk_size)
                    self.downloaded_size += len(chunk)
                    if not chunk:
                        break
                    fp.write(chunk)
            self.ok = True

        def start(self) -> None:
            "启动下载"
            self._thread = Thread(target=self._thread_func,daemon=True)
            self.start()

    class MultiThreadDownloadFile:
        def __init__(self,url:str,savepath:str,tempdir:str,data:object=None,json:JSONData=None,params:ParamsData=None,headers:HttpHeaders=None,maxchunk:int=2*MB,thread_count:int=16,try_count:int=1,writechunk:int=KB,timeout:Union[int,float]=10,context:SSLContext=disabled_ssl_context,method:str=None) -> None:
            '''
            多线程下载单个文件
            :url: URL
            :savepath: 文件保存路径
            :tempdir: 临时文件路径
            :params: url params
            :headers: 请求头
            :maxchunk: 每线程最大分块
            :try_count: 线程请求失败最大尝试次数
            :writechunk: 每次写入最大大小
            :timeout: 超时时间（秒）
            '''
            # 全部下载完成 -> 开始合块 -> 输出文件
            self.method = method
            if not method:
                if data or json:
                    self.method = 'POST'
                else:
                    self.method = 'GET'
            if data and json:
                raise ValueError('"data" parameter and "json" cannot be used together.')
            self.url = urlformat(url,params)
            self.savepath = savepath
            makedirs(tempdir,exist_ok=True)
            self.tmpdir = abspath(tempdir)
            self.headers = headers if headers else {}
            self.maxchunk = maxchunk
            self.try_count = try_count if try_count > 0 else 1
            self.writechunk = writechunk
            self.timeout = timeout
            self.task_id = id_16b
            makedirs(join(self.tmpdir,self.task_id),exist_ok=True) # 创建临时文件夹
            self.thread_count = thread_count
            self.error = [] # 错误
            self.thread_error = [] # 下载失败的线程
            self.context = context
            self.downloaded_size = 0
            "已下载数据大小"
            self.chunk_files = []
            self.ok_threads = 0
            self.threads:List[Thread] = []
            if data or json:
                if data:
                    self.data:str = data
                else:
                    self.data:str = dumps(data,ensure_ascii=False)
            else:
                self.data = None
            if not requests.supports_range_requests(self.url,self.headers,self.timeout):
                raise HostError("对方主机不支持分块下载")
            self.size = self.get_size()
            self.task:List[List[Tuple[int,int]]] = split_list(get_chunks(self.size,self.maxchunk),self.thread_count) # 分块
            # [[(start,end),...],...]
            self.killed = False
            self.step:int = 0
            '当前进行的步骤\n:0.初始化\n:1.下载\n:2.初级合并\n:3.完全合并\n:4.完成\n:-1.失败'

        def kill(self) -> None:
            '''
            强制停止任务
            '''
            self.killed = True

        @property
        def download_thread_count(self) -> int:
            r = 0
            for task in self.task:
                r += len(task)
            return r            

        def download_thread(self,start:int,end:int) -> None:
            "下载线程"
            headers = self.headers
            headers['Range'] = 'bytes=%d-%d'%(start,end)
            err = None
            for _ in range(self.try_count):
                if self.killed:
                    return
                try:
                    req = request.Request(self.url,self.data,headers,method=self.method)
                    res:_UrlopenRet = request.urlopen(req,context=self.context)
                    if self.killed:
                        return
                    while True:
                        with open(join(self.tmpdir,self.task_id,'thread_%s-%s.tmp'%(hex(start),hex(end))),'wb') as fp:
                            d = res.read(self.writechunk)
                            self.downloaded_size += len(d)
                            if self.killed:
                                return
                            if not d:
                                break
                            fp.write(d)
                    self.ok_threads += 1
                    break
                except error.URLError as e:
                    self.error.append(RequestsError(e))
                    err = RequestsError(e)
                except Exception as e:
                    self.error.append(e);err = e
            else:
                self.thread_error.append(err)

        def merge_thread(self,task:List[Tuple[int,int]]) -> None:
            "合并线程下载的文件为块"
            chunkfile = join(self.tmpdir,self.task_id,"chunk_%s-%s.tmp"%(task[0][0],task[-1][-1]))
            self.chunk_files.append(chunkfile)
            with open(chunkfile,'wb') as chunkfp:
                for td in [join(self.tmpdir,self.task_id,"thread_%s-%s.tmp"%(hex(tup[0]),hex(tup[1]))) for tup in task]:
                    with open(td,'rb') as tdfp:
                        while True:
                            if self.killed:
                                return
                            data = tdfp.read(self.writechunk)
                            if not data:
                                break
                            chunkfp.write(data)

        def merge_output(self) -> None:
            "合并块文件为输出文件"
            with open(self.savepath,'wb') as fp:
                for cf in self.chunk_files:
                    with open(cf,'rb') as cfp:
                        while True:
                            if self.killed:
                                return
                            data = cfp.read(self.writechunk)
                            if not data:
                                break
                            fp.write(data)
            
        def create_download_task(self,task:List[Tuple[int,int]]) -> None:
            "创造下载任务"
            for tup in task:
                if self.killed:
                    return
                self.threads.append(Thread(target=self.download_thread,args=(tup[0],tup[1]),daemon=True))
                self.threads[-1].start()

        def wait_download(self) -> None:
            "等待下载线程完成"
            for t in self.threads:
                if self.killed:
                    return
                t.join()

        def download_is_ok(self) -> bool:
            "下载线程完成"
            for t in self.threads:
                if t.is_alive():
                    return True
            else:
                return False
        
        def remove_download_cache(self) -> None:
            "删除下载缓存"
            for task in self.task:
                for fp in [join(self.tmpdir,self.task_id,"thread_%s-%s.tmp"%(hex(tup[0]),hex(tup[1]))) for tup in task]:
                    if isfile(fp):
                        remove(fp)
        
        def remove_chunk_cache(self) -> None:
            "删除合并缓存"
            for fp in self.chunk_files:
                if isfile(fp):
                    remove(fp)

        def get_size(self) -> int:
            "获取文件大小"
            try:
                req = request.Request(self.url,self.data,self.headers,method=self.method)
                res:_UrlopenRet = request.urlopen(req,context=self.context)
                return res.length
            except Exception as e:
                raise RequestsError(e)
            
        def _main(self) -> None:
            #print('main running')
            try:
                self.step = 1
                for task in self.task:
                    self.create_download_task(task)
                    self.wait_download()
                    self.threads = []
                if self.thread_error:
                    return
                # 下载完成 开始合并
                self.step = 2
                for task in self.task:
                    self.merge_thread(task)
                self.step = 3
                self.merge_output()
                self.step = 4
            except Exception as e:
                self.thread_error.append(e)
                self.step = -1
        
        def start(self) -> None:
            thread = Thread(target=self._main,daemon=True)
            thread.start()

        def raise_error(self) -> None:
            if self.thread_error:
                raise self.thread_error[-1]
        
        def get_downloaded_size(self) -> int:
            "获取已下载的大小"
            return self.downloaded_size
            
    18187059.86
    24117248.964
            
    class DownloadMultiFiles:
        class MultiThreadDownloadRequest:
            "多线程下载请求"
            def __init__(self,url:str,path:str,headers:HttpHeaders,params:ParamsData=None,timeout:float=5,try_count:int=1,context:SSLContext=disabled_ssl_context,method:str='GET',writechunk:int=1024,thread_chunk:int=32*KB,thread_count:int=4) -> None:
                '''
                :url: URL
                :path: 保持路径
                :headers: 请求头
                :params: 参数
                :timeout: 超时
                :try_count: 失败最大尝试次数
                :context: SSL Context
                :method: 请求方法
                :writechunk: 写入块大小
                :thread_chunk: 每下载线程最大大小
                :thread_count: 最大线程数量
                '''
                self.url = urlformat(url,params)
                if try_count < 1:
                    raise ValueError("尝试次数不得低于1")
                self.timeout = timeout
                self.path = path
                self.context = context
                self.headers = headers
                self.thread_chunk = thread_chunk
                self.method = method
                self.writechunk = writechunk
                self.try_count = try_count
                self.thread_count = thread_count
        
        class DownloadRequest:
            "单线程下载请求"
            def __init__(self,url:str,path:str,headers:HttpHeaders,params:ParamsData=None,timeout:float=5,try_count:int=1,context:SSLContext=disabled_ssl_context,method:str='GET',writechunk:int=1024) -> None:
                '''
                :url: URL
                :path: 保存路径
                :headers: 请求头
                :params: 参数
                :timeout: 超时
                :try_count: 失败最大尝试次数
                :context: SSL Context
                :method: 请求方法
                :writechunk: 写入块大小
                '''
                self.url = urlformat(url,params)
                if try_count < 1:
                    raise ValueError("尝试次数不得低于1")
                self.timeout = timeout
                self.path = path
                self.context = context
                self.headers = headers
                self.method = method
                self.try_count = try_count
                self.writechunk = writechunk

        class _Task:
            def __init__(self) -> None:self.size = 0;self.ok = False
            def __call__(self) -> bool:return self.ok
                
        def __init__(self,*reqs:Union[MultiThreadDownloadRequest,DownloadRequest],max_multithread_task:int=16,max_onethread_task:int=32,tmpdir:str) -> None:
            '''
            :*reqs: 下载请求
            :max_multithread_task: 最大同时进行的多线程下载任务数量
            :max_onethread_task: 最大同时进行的单线程下载任务数量
            '''
            self.reqs = reqs
            self.mttask_count = max_multithread_task
            self.ottask_count = max_onethread_task
            self.ok = False
            self.killed = False
            for _ in range(640):
                self.task_id = id_16b()
                if not isdir(join(tmpdir,self.task_id)):
                    self.tmpdir = join(tmpdir,self.task_id)
                    break
            else:
                raise FileExistsError("无法获取可用的任务id，请尝试清理启动器垃圾")
            self.tasks_mt:List[Thread] = []
            self.tasks_ot:List[Thread] = []
            self.tasks_mt2:List[List[Thread]] = []
            self.tasks_ot2:List[List[Thread]] = []
            self.error = []
            self.downloaded_size = 0
            class _TaskType:
                def __init__(self) -> None:self.size = 0;self.ok = False
                def __call__(self) -> bool:return self.ok
            self.task_threads:Dict[int,_TaskType] = {}

        def all_ok(self) -> bool:
            "所有任务完成"
            return min([v.ok for k,v in self.task_threads.items()])

        def start(self) -> None:
            "启动下载"
            Thread(self._main).start()
            
        def _main(self) -> None:
            "主线程"
            for r in self.reqs:
                if type(r) == self.MultiThreadDownloadRequest:
                    self.tasks_mt.append(Thread(target=self.multithread_task,kwargs={"req":r}))
                else:
                    self.tasks_ot.append(Thread(target=self.onethread_task,kwargs={"req":r}))
            self.tasks_mt2:List[List[Thread]] = split_list(self.tasks_mt,self.mttask_count)
            self.tasks_ot2:List[List[Thread]] = split_list(self.tasks_ot,self.ottask_count)
            for mt_tasks in self.tasks_mt2: # 先启动多线程下载任务
                for task in mt_tasks:
                    task.start()
                    if self.killed:
                        return
                for task in mt_tasks:
                    if self.killed:
                        return
                    task.join()
            for ot_tasks in self.tasks_ot2: # 再启动单线程下载任务
                for task in ot_tasks:
                    task.start()
                    if self.killed:
                        return
                for task in ot_tasks:
                    if self.killed:
                        return
                    task.join()
        
        def multithread_task(self,req:MultiThreadDownloadRequest) -> None:
            "多线程下载任务"
            self_id = get_ident()
            thread_taskid = str(self_id)+id_16b()
            self.task_threads[self_id] = self._Task()
            self.task_threads[self_id].size = 0
            self.task_threads[self_id].ok = False
            thread = requests.MultiThreadDownloadFile(
                req.url,req.path,join(self.tmpdir,thread_taskid),None,None,None,req.headers,
                req.thread_chunk,req.thread_count,req.try_count,
                req.writechunk,req.timeout,req.context,req.method)
            thread.start()
            while True:
                if self.killed:
                    thread.kill()
                    return
                if thread.step == 4:
                    break
                elif thread.step == -1:
                    try:
                        thread.raise_error()
                    except Exception as e:
                        self.error.append(e)
                    else:
                        self.error.append(RequestsError("下载失败"))
                    return
                self.task_threads[self_id].size = thread.downloaded_size

        def onethread_task(self,req:DownloadRequest) -> None:
            "单线程下载任务"
            self_id = get_ident()
            self.task_threads[self_id] = self._Task()
            self.task_threads[self_id].size = 0
            self.task_threads[self_id].ok = False


if __name__ == "__main__":
    ...