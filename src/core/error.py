from urllib import error as _error

#region NetException
class CFApiKeyNotFoundError(Exception):
    "找不到curseforge apikey"
class ModNotFoundError(Exception):
    "找不到mod"
class RequestsError(_error.URLError):
    "net错误基类"
class HttpGetError(RequestsError):
    "请求错误"
class DownloadError(RequestsError):
    "下载错误"
class StatusError(RequestsError):
    "状态码错误"
class HostNotFoundError(RequestsError):
    "找不到主机"
class HttpTimeOutError(RequestsError):
    "请求超时"
class HostError(RequestsError):
    "主机错误"
#endregion

class ProcessExitCodeError(Exception):
    "进程状态码错误"

class Err3582_490(Exception):0

class RepeatTaskError(Exception):
    "重复任务错误"

class FrequentVisitsError(Exception):
    "访问太频繁"

#region MinecraftException
class MinecraftVersionError(Exception):
    "MC版本不正确"
class JSONTypeError(Exception):
    "JSON类型不正确"
class CompatibilityError(Exception):
    "兼容性错误"
#endregion