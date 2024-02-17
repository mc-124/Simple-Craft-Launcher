'''
# pyperclip 修改
* 此模块不会进行维护
--------
修改内容：
:修改判断系统方式（platform改为sys）
:删除qt与gtk部分
:使代码更小
:删除兼容python2.x部分
:__init__.py改为pyperclip.py
:删去__main__.py
:跟随SCL使用MIT LICENT
--------
原开源协议：
BSD LICENT
原作者：[Al Sweigart](mailto:al@inventwithpython.com)
'''
import contextlib,ctypes,os,subprocess,sys,time,platform;from ctypes import c_size_t,sizeof,c_wchar_p,get_errno,c_wchar;HAS_DISPLAY=os.getenv("DISPLAY",False);EXCEPT_MSG="\nPyperclip could not find a copy/paste mechanism for your system.\nFor more information,please visit https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error";STR_OR_UNICODE=str;ENCODING='utf-8';__version__='1.8.2'
try:from shutil import which as _executable_exists
except ImportError:
 if sys.platform=='win32':WHICH_CMD='where'
 else:WHICH_CMD='which'
 def _executable_exists(name):return subprocess.call([WHICH_CMD,name],stdout=subprocess.PIPE,stderr=subprocess.PIPE)==0
class PyperclipException(RuntimeError):pass
class PyperclipWindowsException(PyperclipException):
 def __init__(self,message):message+=" (%s)"%ctypes.WinError();super(PyperclipWindowsException,self).__init__(message)
class PyperclipTimeoutException(PyperclipException):pass
def _stringifyText(text):
 acceptedTypes=(str,int,float,bool)
 if not isinstance(text,acceptedTypes):raise PyperclipException('only str, int, float, and bool values can be copied to the clipboard, not %s'%(text.__class__.__name__))
 return STR_OR_UNICODE(text)
def init_osx_pbcopy_clipboard():
 def copy_osx_pbcopy(text):text=_stringifyText(text);p=subprocess.Popen(['pbcopy','w'],stdin=subprocess.PIPE,close_fds=True);p.communicate(input=text.encode(ENCODING))
 def paste_osx_pbcopy():p=subprocess.Popen(['pbpaste','r'],stdout=subprocess.PIPE,close_fds=True);stdout,stderr=p.communicate();return stdout.decode(ENCODING)
 return copy_osx_pbcopy,paste_osx_pbcopy
def init_osx_pyobjc_clipboard():
 def copy_osx_pyobjc(text):text=_stringifyText(text);newStr=Foundation.NSString.stringWithString_(text).nsstring();newData=newStr.dataUsingEncoding_(Foundation.NSUTF8StringEncoding);board=AppKit.NSPasteboard.generalPasteboard();board.declareTypes_owner_([AppKit.NSStringPboardType],None);board.setData_forType_(newData,AppKit.NSStringPboardType)
 def paste_osx_pyobjc():board=AppKit.NSPasteboard.generalPasteboard();content=board.stringForType_(AppKit.NSStringPboardType);return content
 return copy_osx_pyobjc,paste_osx_pyobjc
def init_gtk_clipboard():pass
def init_qt_clipboard():pass
def init_xclip_clipboard():
 DEFAULT_SELECTION,PRIMARY_SELECTION='c','p'
 def copy_xclip(text,primary=False):
  text,selection=_stringifyText(text),DEFAULT_SELECTION
  if primary:selection=PRIMARY_SELECTION
  p=subprocess.Popen(['xclip','-selection',selection],stdin=subprocess.PIPE,close_fds=True);p.communicate(input=text.encode(ENCODING))
 def paste_xclip(primary=False):
  selection=DEFAULT_SELECTION
  if primary:selection=PRIMARY_SELECTION
  p=subprocess.Popen(['xclip','-selection',selection,'-o'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True);stdout,stderr=p.communicate();return stdout.decode(ENCODING)
 return copy_xclip,paste_xclip
def init_xsel_clipboard():
 DEFAULT_SELECTION='-b'
 PRIMARY_SELECTION='-p'
 def copy_xsel(text,primary=False):
  text=_stringifyText(text);selection_flag=DEFAULT_SELECTION
  if primary:selection_flag=PRIMARY_SELECTION
  p=subprocess.Popen(['xsel',selection_flag,'-i'],stdin=subprocess.PIPE,close_fds=True);p.communicate(input=text.encode(ENCODING))
 def paste_xsel(primary=False):
  selection_flag=DEFAULT_SELECTION
  if primary:selection_flag=PRIMARY_SELECTION
  p=subprocess.Popen(['xsel',selection_flag,'-o'],stdout=subprocess.PIPE,close_fds=True);stdout,_=p.communicate();return stdout.decode(ENCODING)
 return copy_xsel,paste_xsel
def init_wl_clipboard():
 PRIMARY_SELECTION="-p"
 def copy_wl(text,primary=False):
  text=_stringifyText(text);args=["wl-copy"]
  if primary:args.append(PRIMARY_SELECTION)
  if not text:args.append('--clear');subprocess.check_call(args,close_fds=True)
  else:p=subprocess.Popen(args,stdin=subprocess.PIPE,close_fds=True);p.communicate(input=text.encode(ENCODING))
 def paste_wl(primary=False):
  args=["wl-paste","-n"]
  if primary:args.append(PRIMARY_SELECTION)
  p=subprocess.Popen(args,stdout=subprocess.PIPE,close_fds=True);stdout,_=p.communicate();return stdout.decode(ENCODING)
 return copy_wl,paste_wl
def init_klipper_clipboard():
 def copy_klipper(text):
  text=_stringifyText(text)
  p=subprocess.Popen(['qdbus','org.kde.klipper','/klipper','setClipboardContents',text.encode(ENCODING)],stdin=subprocess.PIPE,close_fds=True)
  p.communicate(input=None)
 def paste_klipper():
  p=subprocess.Popen(['qdbus','org.kde.klipper','/klipper','getClipboardContents'],stdout=subprocess.PIPE,close_fds=True)
  stdout,_=p.communicate();clipboardContents=stdout.decode(ENCODING);assert len(clipboardContents)>0;assert clipboardContents.endswith('\n')
  if clipboardContents.endswith('\n'):clipboardContents=clipboardContents[:-1]
  return clipboardContents
 return copy_klipper,paste_klipper
def init_dev_clipboard_clipboard():
 def copy_dev_clipboard(text):
  text=_stringifyText(text)
  if text=='':pass
  if'\r' in text:pass
  fo=open('/dev/clipboard','wt');fo.write(text);fo.close()
 def paste_dev_clipboard():fo=open('/dev/clipboard','rt');content=fo.read();fo.close();return content
 return copy_dev_clipboard,paste_dev_clipboard
def init_no_clipboard():
 class ClipboardUnavailable(object):
  def __call__(self,*args,**kwargs):raise PyperclipException(EXCEPT_MSG)
  def __bool__(self):return False
 return ClipboardUnavailable(),ClipboardUnavailable()
class CheckedCall(object):
 def __init__(self,f) -> None:super(CheckedCall,self).__setattr__("f",f)
 def __call__(self,*args):
  ret=self.f(*args)
  if not ret and get_errno():raise PyperclipWindowsException("Error calling "+self.f.__name__)
  return ret
 def __setattr__(self,key,value):setattr(self.f,key,value)
def init_windows_clipboard():
 global HGLOBAL,LPVOID,DWORD,LPCSTR,INT,HWND,HINSTANCE,HMENU,BOOL,UINT,HANDLE;from ctypes.wintypes import HGLOBAL,LPVOID,DWORD,LPCSTR,INT,HWND,HINSTANCE,HMENU,BOOL,UINT,HANDLE;windll=ctypes.windll;msvcrt=ctypes.CDLL('msvcrt');safeCreateWindowExA=CheckedCall(windll.user32.CreateWindowExA);safeCreateWindowExA.argtypes=[DWORD,LPCSTR,LPCSTR,DWORD,INT,INT,INT,INT,HWND,HMENU,HINSTANCE,LPVOID];safeCreateWindowExA.restype=HWND;safeDestroyWindow=CheckedCall(windll.user32.DestroyWindow);safeDestroyWindow.argtypes=[HWND];safeDestroyWindow.restype=BOOL;OpenClipboard=windll.user32.OpenClipboard;OpenClipboard.argtypes=[HWND];OpenClipboard.restype=BOOL;safeCloseClipboard=CheckedCall(windll.user32.CloseClipboard);safeCloseClipboard.argtypes=[];safeCloseClipboard.restype=BOOL;safeEmptyClipboard=CheckedCall(windll.user32.EmptyClipboard);safeEmptyClipboard.argtypes=[];safeEmptyClipboard.restype=BOOL;safeGetClipboardData=CheckedCall(windll.user32.GetClipboardData);safeGetClipboardData.argtypes=[UINT];safeGetClipboardData.restype=HANDLE;safeSetClipboardData=CheckedCall(windll.user32.SetClipboardData);safeSetClipboardData.argtypes=[UINT,HANDLE];safeSetClipboardData.restype=HANDLE;safeGlobalAlloc=CheckedCall(windll.kernel32.GlobalAlloc);safeGlobalAlloc.argtypes=[UINT,c_size_t];safeGlobalAlloc.restype=HGLOBAL;safeGlobalLock=CheckedCall(windll.kernel32.GlobalLock);safeGlobalLock.argtypes=[HGLOBAL];safeGlobalLock.restype=LPVOID;safeGlobalUnlock=CheckedCall(windll.kernel32.GlobalUnlock);safeGlobalUnlock.argtypes=[HGLOBAL];safeGlobalUnlock.restype=BOOL;wcslen=CheckedCall(msvcrt.wcslen);wcslen.argtypes=[c_wchar_p];wcslen.restype=UINT;GMEM_MOVEABLE=0x0002;CF_UNICODETEXT=13
 @contextlib.contextmanager
 def window():
  hwnd=safeCreateWindowExA(0,b"STATIC",None,0,0,0,0,0,None,None,None,None)
  try:yield hwnd
  finally:safeDestroyWindow(hwnd)
 @contextlib.contextmanager
 def clipboard(hwnd):
  t=time.time()+0.5;success=False
  while time.time()<t:
   success=OpenClipboard(hwnd)
   if success:break
   time.sleep(0.01)
  if not success:raise PyperclipWindowsException("Error calling OpenClipboard")
  try:yield
  finally:safeCloseClipboard()
 def copy_windows(text):
  text=_stringifyText(text)
  with window()as hwnd:
   with clipboard(hwnd):
    safeEmptyClipboard()
    if text:count=wcslen(text)+1;handle=safeGlobalAlloc(GMEM_MOVEABLE,count * sizeof(c_wchar));locked_handle=safeGlobalLock(handle);ctypes.memmove(c_wchar_p(locked_handle),c_wchar_p(text),count * sizeof(c_wchar));safeGlobalUnlock(handle);safeSetClipboardData(CF_UNICODETEXT,handle)
 def paste_windows():
  with clipboard(None):
   handle=safeGetClipboardData(CF_UNICODETEXT)
   if not handle:return ""
   return c_wchar_p(handle).value
 return copy_windows,paste_windows
def init_wsl_clipboard():
 def copy_wsl(text):text=_stringifyText(text);p=subprocess.Popen(['clip.exe'],stdin=subprocess.PIPE,close_fds=True);p.communicate(input=text.encode(ENCODING))
 def paste_wsl():p=subprocess.Popen(['powershell.exe','-command','Get-Clipboard'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True);stdout,_=p.communicate();return stdout[:-2].decode(ENCODING)
 return copy_wsl,paste_wsl
def determine_clipboard():
 global Foundation,AppKit
 if'cygwin'in platform.system().lower():
  if os.path.exists('/dev/clipboard'):return init_dev_clipboard_clipboard()
 elif sys.platform=='win32':return init_windows_clipboard()
 if sys.platform=='linux' and os.path.isfile('/proc/version'):
  with open('/proc/version','r')as f:
   if"microsoft" in f.read().lower():return init_wsl_clipboard()
 if sys.platform=='darwin':
  try:import Foundation, AppKit
  except ImportError:return init_osx_pbcopy_clipboard()
  else:return init_osx_pyobjc_clipboard()
 if HAS_DISPLAY:
  if os.environ.get("WAYLAND_DISPLAY") and _executable_exists("wl-copy"):return init_wl_clipboard()
  if _executable_exists("xsel"):return init_xsel_clipboard()
  if _executable_exists("xclip"):return init_xclip_clipboard()
  if _executable_exists("klipper") and _executable_exists("qdbus"):return init_klipper_clipboard()
 return init_no_clipboard()
def set_clipboard(clipboard):
 global copy,paste;clipboard_types={"pbcopy":init_osx_pbcopy_clipboard,"pyobjc":init_osx_pyobjc_clipboard,"gtk":init_gtk_clipboard,"qt":init_qt_clipboard,"xclip":init_xclip_clipboard,"xsel":init_xsel_clipboard,"wl-clipboard":init_wl_clipboard,"klipper":init_klipper_clipboard,"windows":init_windows_clipboard,"no":init_no_clipboard,}
 if clipboard not in clipboard_types:raise ValueError('Argument must be one of %s'%(','.join([repr(_) for _ in clipboard_types.keys()])))
 copy,paste=clipboard_types[clipboard]()
def lazy_load_stub_copy(text):global copy,paste;copy,paste=determine_clipboard();return copy(text)
def lazy_load_stub_paste():global copy,paste;copy,paste=determine_clipboard();return paste()
def is_available():return copy != lazy_load_stub_copy and paste != lazy_load_stub_paste
copy,paste=lazy_load_stub_copy,lazy_load_stub_paste
def waitForPaste(timeout=None):
 startTime=time.time()
 while True:
  clipboardText=paste()
  if clipboardText != '':return clipboardText
  time.sleep(0.01)
  if timeout is not None and time.time()>startTime+timeout:raise PyperclipTimeoutException('waitForPaste() timed out after '+str(timeout)+' seconds.')
def waitForNewPaste(timeout=None):
 startTime=time.time();originalText=paste()
 while True:
  currentText=paste()
  if currentText != originalText:return currentText
  time.sleep(0.01)
  if timeout is not None and time.time()>startTime+timeout:raise PyperclipTimeoutException('waitForNewPaste() timed out after '+str(timeout)+' seconds.')
