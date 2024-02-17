'''
### tkinter控件
'''
from tkinter import Canvas,Tk,Toplevel,Label,Widget,PhotoImage,Frame,Button,Event,Entry,Scrollbar,StringVar
from tkinter.ttk import Combobox,Radiobutton
from tkinter.font import Font
from threading import Thread
from types import FunctionType as Function
from os.path import join
from time import sleep
import sys
from typing import List,Tuple,Union
from typing_extensions import Literal
from threading import Thread
from core.utils import Match

NoneType = type(None)
WindowType = Union[Tk,Frame]
NoneFunc = lambda:None

# BUG: MainWindow: 无法调整大小
# BUG：MainWindow: tkinter在新建窗体时如果隐藏了标题栏在windows中会导致任务栏不显示窗体图标。已经尝试修复，但是如果启动时焦点不在程序仍然会导致任务栏不显示图标 有没有哪个tkinter好的来FIXME...

# region tkinter-string-values
ACTIVE = 'active'
DISABLED = 'disabled'
# XXX 错误的 ENABLED = 'enabled'
ALL = 'all'
END = 'end'
NORMAL = 'normal'
INFO = 'info'
QUESTION = 'question'
WARNING = 'warning'
ERROR = 'error'
X = 'x'
Y = 'y'
START = 1.0
BOTH = 'both'
N = 'n'
CENTER = 'center'
NW = 'nw'
HIDDEN = 'hidden'
LEFT = 'left'
RIGHT = 'right'
ALPHA = '-alpha'
# endregion

class MouseCursor:
    arrow = 'arrow'
    "箭头"
    hand2 = 'hand2'
    "点击"
    xterm = 'xterm'
    "输入"
    no = 'no'
    "禁止"

class Binds:
    "tkinter bind事件字符串"
    Button1         :str = '<Button-1>'
    '鼠标左键单击'
    Button2         :str = '<Button-2>'
    "鼠标中键单击"
    Button3         :str = '<Button-3>'
    "鼠标右键单击"
    DoubleButton1   :str = '<Double-Button-1>'
    "鼠标左键双击"
    DoubleButton2   :str = '<Double-Button-2>'
    "鼠标中键双击"
    DoubleButton3   :str = '<Double-Button-3>'
    "鼠标右键双击"
    TripleButton1   :str = '<Triple-Button-1>'
    "鼠标左键三击"
    TripleButton2   :str = '<Triple-Button-2>'
    "鼠标中键三击"
    TripleButton3   :str = '<Triple-Button-3>'
    "鼠标右键三击"
    Motion          :str = '<Motion>'
    "鼠标移动"
    Enter           :str = '<Enter>'
    "鼠标进入控件"
    Leave           :str = '<Leave>'
    "鼠标离开控件"
    FocusIn         :str = '<FocusIn>'
    "键盘焦点获得"
    FocusOut        :str = '<FocusOut>'
    "键盘焦点失去"
    Return          :str = '<Return>'
    "键盘回车"
    Key             :str = '<Key>'
    "键盘按下"
    KeyRelease      :str = '<KeyRelease>'
    "键盘松开"
    Configure       :str = '<Configure>'
    "窗口配置修改"
    Destroy         :str = '<Destroy>'
    "控件被销毁"
    Visibility      :str = '<Visibility>'
    "控件变为可见"
    MouseWheel      :str = '<MouseWheel>'
    "滚轮滚动"
    ButtonPress1    :str = '<ButtonPress-1>'
    "鼠标左键按下"
    ButtonPress2    :str = '<ButtonPress-2>'
    "鼠标中键按下"
    ButtonPress3    :str = '<ButtonPress-3>'
    "鼠标右键按下"
    ButtonRelease1  :str = '<ButtonRelease-1>'
    "鼠标左键释放"
    ButtonRelease2  :str = '<ButtonRelease-2>'
    "鼠标中键释放"
    ButtonRelease3  :str = '<ButtonRelease-3>'
    "鼠标右键释放"

def _geometry(root:Tk,width:int,height:int) -> None:
    '''
    在屏幕中心放置窗体 用于代替Tk.geometry
    :width: Tk宽
    :height: Tk高
    '''
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    root.geometry("%dx%d+%d+%d" % (width,height,x,y))

class LoadingAnim(Label): # ttk.Label切换图片过于缓慢
    '加载中的转圈动画'
    def __init__(self,master:Widget,imgdir:str,range_start:int=0,range_end:int=120,bg:str=None,range_name:str='loading-{i}.gif',delay:float=0.0334,**kw) -> None:
        '''
        :master: 窗体
        :imgdir: 图片路径
        :range_start: range 开始
        :range_end: range 结束
        :bg: 背景颜色
        :range_name: 每张图的名字 要用{i}
        :delay: 切换图片间隔 0.334约等于30fps
        :kw: Label的其他参数
        '''
        images_path = [range_name.format(i=i) for i in range(range_start,range_end)]
        self.images = []
        for img in images_path:
            self.images.append(PhotoImage(file=join(imgdir,img)))
        # 提前将图片加载进内存 避免多手的人删除导致错误 200kb的图片应该不会占用太多内存
        super().__init__(master,bg=bg,image=self.images[0])
        self.running = False
        self.thread = None
        self.delay = delay
        self.error = None

    def _thread(self) -> None:
        while True:
            if not self.running:
                break
            try:
                for g in self.images:
                    sleep(self.delay)
                    self.config(image=g)
            except Exception as e:
                self.error = e
                break
    
    def start(self) -> None:
        '启动线程'
        if self.running:
            raise RuntimeError('已有一个线程在运行')
        self.running = True
        self.thread = Thread(target=self._thread,daemon=True)
        self.thread.start()

    def stop(self) -> None:
        '停止线程'
        self.running = False
    
    def raise_error(self) -> None:
        '若线程出现错误，调用此函数可抛出'
        if self.error:
            e = self.error
            self.error = None
            raise e
        
    def destroy(self) -> None:
        '销毁'
        self.running = False
        self.images = None # 清理PhotoImage
        return super().destroy()

class rgb:
    def __init__(self,Hex:str=None,r:int=0,g:int=0,b:int=0) -> None:
        self.r = abs(r) if abs(r) in range(256) else 255
        self.g = abs(g) if abs(g) in range(256) else 255
        self.b = abs(b) if abs(b) in range(256) else 255
        
        if Hex:
            self.r,self.g,self.b = rgb._hex_to_rgb(Hex)

    def _hex_to_rgb(Hex:str) -> Tuple[int,int,int]:
        if not Hex.startswith('#') or len(Hex) != 7:
            raise ValueError("format error")
        r = int(Hex[1:3],16)
        g = int(Hex[3:5],16)
        b = int(Hex[5:7],16)
        return (r,g,b)
    
    def _rgb_to_hex(r:int=0,g:int=0,b:int=0) -> str:
        if r not in range(256) or g not in range(256) or b not in range(256):
            raise ValueError('The RGB value cannot be greater than 255 or less than 0')
        red =   hex(r)[2:].upper()if len(hex(r)[2:])==2 else'0'+hex(r)[2:].upper()
        green = hex(g)[2:].upper()if len(hex(g)[2:])==2 else'0'+hex(g)[2:].upper()
        blue =  hex(b)[2:].upper()if len(hex(b)[2:])==2 else'0'+hex(b)[2:].upper()
        if len(red)   > 2:red   = 'FF'
        if len(green) > 2:green = 'FF'
        if len(blue)  > 2:blue  = 'FF'
        return '#%s%s%s'%(red,green,blue)
    
    def format_tuple(self) -> Tuple[int,int,int]:
        return (self.r,self.g,self.b)
    
    def format_hex(self) -> str:
        return rgb._rgb_to_hex(self.r,self.g,self.b)
    
    def __sub__(self,other):
        if isinstance(other,rgb):
            tup0 = self.format_tuple()
            tup1 = other.format_tuple()
            tup = (tup0[0]-tup1[0],tup0[1]-tup1[1],tup0[2]-tup1[2])
            return rgb(r=tup[0],g=tup[1],b=tup[2])
        else:
            raise TypeError("Expected 'rgb' instance, got %s"%type(other).__name__)
        
    def __add__(self,other):
        if isinstance(other,rgb):
            tup0 = self.format_tuple()
            tup1 = other.format_tuple()
            tup = (tup0[0]+tup1[0],tup0[1]+tup1[1],tup0[2]+tup1[2])
            return rgb(r=tup[0],g=tup[1],b=tup[2])
        else:
            raise TypeError("Expected 'rgb' instance, got %s"%type(other).__name__)

class ScrollableFrame(Frame):
    "滚动容器"
    def __init__(self,master:Widget,width:int=400,height:int=400,widgets:List[Widget]=[],**kw):
        super().__init__(master,**kw)
        self.canvas = Canvas(self,width=width,height=height)
        self.bar = Scrollbar(self,command=self.canvas.yview)
        self.frame = Frame(self.canvas)
        self.bar.pack(side="right",fill="y")
        self.canvas.pack(side="left",fill="both",expand=True)
        self.frame.pack()
        self.canvas.create_window(0,0,window=self.frame,anchor='nw')
        self.canvas.config(yscrollcommand=self.bar.set)
        self.canvas.bind_all(Binds.MouseWheel,self._mousewheel)
        self.frame.bind(Binds.Configure,self._frame_configure)
    
    def _mousewheel(self,e:Event) -> None:
        self.canvas.yview_scroll(int(-1*(e.delta/60)),'units')

    def _frame_configure(self,e:Event) -> None:
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def add_widget(self,widget:Widget) -> None:
        widget.pack(fill='x')

    def __call__(self) -> Frame:
        return self.frame

class Tooltip:
    "控件提示文本"
    def __init__(self,widget:Widget,text:str,delay:int=500) -> None:
        '''
        :widget: 控件
        :text: 提示文本
        :delay: 显示延迟
        '''
        self.widget,self.text = widget,text
        self.tooltip = None
        self.delay = delay
        self._id = None
        self.bind_enter = self.widget.bind(Binds.Enter,self.schedule,add='+')
        self.bind_leave = self.widget.bind(Binds.Leave,self.hide_tooltip,add='+')

    def schedule(self,e) -> None:
        "调用显示"
        self._id = self.widget.after(self.delay,self.show_tooltip)

    def show_tooltip(self) -> None:
        "显示"
        if self.tooltip:
            self.tooltip.destroy()
        self.tooltip = tooltip_win = Toplevel(self.widget)
        tooltip_win.wm_overrideredirect(True)
        label = Label(tooltip_win,text=self.text,background="#ffffff",relief="solid",bd=1)
        label.pack()
        x = self.widget.winfo_rootx() + 15
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        tooltip_win.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self,e) -> None:
        "隐藏"
        if self._id:
            self.widget.after_cancel(self._id)
            self._id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
    
    def destroy(self) -> None:
        "删除"
        self.widget.unbind(Binds.Enter,self.bind_enter)
        self.widget.unbind(Binds.Leave,self.bind_leave)
        self.hide_tooltip(None)
        self.widget = None
        self.text = None

class SlideButton(Canvas):
    '## 开关控件\n\n由 [[github:FMCL]](https://github.com/Sharll-large/FMCL) 项目的`FMCLView.tk_extend.slide_button.SlideButton`更改'
    def __init__(self,master:Tk=None,width:int=80,thick:int=25,state:str=NORMAL,command:Function=None,anispeed:float=0.2,disabled_animation:bool=False,bg:str='#ffffff',fg:str='#000000',n_bg:str=None,n_fg:str=None,d_fg:str='#999999',d_bg:str='#000000',default_state:bool=False) -> None:
        '''
        :master: 窗体
        :width: 控件宽
        :thick: 控件高
        :state: 控件状态
        :command: 被点击时触发的函数
        :anispeed: 动画速度
        :disabled_animation: 禁用动画
        '''
        super().__init__(master=master,width=width,height=thick,bd=0)
        self.state = NORMAL
        self.width = width
        self.thick = thick
        self.bg = bg
        self.fg = fg
        self._bg = bg
        self._fg = fg
        self.d_fg = d_fg
        self.normal_bg = n_bg or bg
        self.normal_fg = n_fg or fg
        if anispeed <= 0 or anispeed >= 1:
            raise ValueError('anispeed error')
        self.anispeed = anispeed if not disabled_animation else 1
        self.b_state = state
        self.running = False
        self.click_func = command
        if self.b_state == DISABLED:
            self.fg = d_fg
        if state == ACTIVE:
            self.draw(int(width - thick))
        else:
            self.draw(0)
        self.bind(Binds.Button1,self.onclick)

    def draw(self,pos=0) -> None:
        self.delete(ALL)
        self.create_rectangle(0,0,self.width+5,self.thick+5,fill=self.bg)
        self.create_line(self.thick/2,self.thick/2,self.width-self.thick/2,self.thick/2,capstyle="round",fill=self.fg,width=self.thick)
        self.create_line(self.thick/2,self.thick/2,self.width-self.thick/2,self.thick/2,capstyle="round",fill=self.bg,width=self.thick-5)
        self.create_line(self.thick/2+pos,self.thick/2,self.thick/2+pos,self.thick/2,capstyle="round",fill=self.fg,width=self.thick-10)

    def change_state(self,b_state:str) -> None:
        """
        更改控件状态
        :b_state: tkinter状态字符串
        """
        self.b_state = b_state
        if b_state == DISABLED:
            self.fg = self.d_fg
        else:
            self.fg = self._fg
        if self.b_state == ACTIVE:
            self.draw(self.width - self.thick)
        else:
            self.draw(0)

    def set(self,value:bool) -> None:
        '''
        设置开关状态
        :value: 状态
        '''
        if value:
            self.state = ACTIVE
            self.draw(self.width - self.thick)
        else:
            self.state = NORMAL
            self.draw(0)

    def get(self) -> None:
        '获取开关状态'
        if self.state == ACTIVE:
            return True
        else:
            return False

    def onclick(self,_) -> None:
        if self.running:
            return
        if self.b_state == NORMAL:
            self.running = True
            if self.state == NORMAL:
                self.state = ACTIVE
                def _flush(p):
                    return lambda: self.draw(poses[p])
                pos = 0
                poses = []
                max_pos = int(self.width - self.thick)
                while round(pos) != max_pos:
                    poses.append(pos)
                    pos += (max_pos - pos) * self.anispeed
                poses.append(max_pos)
                for i in range(len(poses)):
                    self.after(i * 20,_flush(i))
                self.after(len(poses) * 20,lambda:setattr(self,'running',False))
                self.draw(max_pos)
            else:
                self.state = NORMAL
                def _flush(p):
                    return lambda: self.draw(poses[p])
                pos = int(self.width - self.thick)
                poses = []
                max_pos = 0
                while round(pos) != max_pos:
                    poses.append(pos)
                    pos += (max_pos - pos) * self.anispeed
                poses.append(max_pos)
                for i in range(len(poses)):
                    self.after(i * 20,_flush(i))
                self.after(len(poses) * 20,lambda: setattr(self,'running',False))
                self.draw(max_pos)
            if self.click_func:
                self.click_func(self.state==ACTIVE)

    def ani_config(self,width:int=None,thick:int=None,state:str=None,command:Function=None,anispeed:float=None,disabled_animation:bool=None,bg:str=None,fg:str=None,n_bg:str=None,n_fg:str=None,d_fg:str=None) -> None:
        if anispeed <= 0 or anispeed >= 1:
            raise ValueError('anispeed error')
        self.width = width or self.width
        self.thick = thick or self.thick
        self.b_state = state or self.b_state
        self.click_func = command or self.click_fun
        self.anispeed = anispeed or self.anispeed
        if type(disabled_animation)!=NoneType:
            self.anispeed = 0 if disabled_animation else self.anispeed
        self._bg = bg or self._bg
        self._fg = fg or self._fg
        self.normal_fg = n_fg or self.normal_fg
        self.normal_bg = n_bg or self.normal_bg
        self.d_fg = d_fg or self.d_fg
        self.config(height=self.thick,width=self.width)
        if self.b_state == ACTIVE:
            self.draw(self.width - self.thick)
        else:
            self.draw(0)

class colors:
    def __init__(self) -> None:
        self.bg0 = '' # 正常颜色
        self.bg1 = '' # 浅色(float)
        self.bg2 = '' # 深色(press/active)
        self.bg3 = '' # 浅色(disabled)
        self.fg0 = '' # 正常颜色
        self.fg1 = '' # 浅色(active)
        self.fg2 = '' # 浅色(disabled)

class MainWindow(Tk):
    def __init__(self,disabled_animation:bool=False,delay:int=4,index_frame:Frame=None,frames:list=[],window_transp:float=1.0,title:str='',geometry:str=None,window_close_command:Function=None,colorobj:colors=None):
        '''
        :disabled_animation: 禁用动画
        :delay: 动画长度
        :index_frame: 首页
        :frames: 页面
        :window_transp: 透明度
        :title: 窗体标题
        :geometry: 大小
        :window_close_command: 窗体关闭函数
        :anidelay: 动画速度
        '''
        super().__init__()
        self.resizable(False,False) # 反正有BUG导致无法调大小，干脆就禁用了
        if colorobj:
            self.color = colorobj
        else:
            self.color = colors()
            self.color.bg0 = '#0084d0'
            self.color.bg1 = '#23a8f2'
            self.color.bg2 = '#1f7caf'
            self.color.bg3 = '#8bd5ff'
            self.color.fg0 = '#ffffff'
            self.color.fg1 = '#eeeeee'
            self.color.fg2 = '#bbbbbb'
        if sys.platform == 'win32':
            self.font = Font(family='Segou UI')
        _frames = {}
        print(frames)
        for f in frames:
            _frames[f] = f(self)
        self.Frame:dict[object,Frame] = {} if not frames else _frames
        self._index_frame:Widget = index_frame
        self.running = False
        self.Hint = HintBox(self)
        self.head = WindowHead(self)
        self.head.pack(anchor=N,fill=X,expand=1)
        self.anidelay = delay
        self.window_x = None
        self.window_y = None
        if title:self.title(title)
        if geometry:
            _geometry(self,int(geometry.split('x')[0]),int(geometry.split('x')[-1]))
        self.overrideredirect(True) 
        self.window_close_command = window_close_command or NoneFunc
        self.disabled_ani = disabled_animation
        self.window_transp = window_transp
        self.attributes('-alpha',0)
        self.now_show = None
        self.add_frame(NoneFrame)
        self.show(NoneFrame,'no')
        if self._index_frame not in self.Frame and self._index_frame:
            self.add_frame(self._index_frame)

    def minisize(self) -> None:
        self.iconify()
    
    def de_minisize(self) -> None:
        self.deiconify()

    def _start_move(self,e:object) -> None: # 开始移动窗体
        self.window_x = e.x
        self.window_y = e.y

    def _do_move(self,e:object) -> None: # 移动窗体
        dx = e.x-self.window_x
        dy = e.y-self.window_y
        x = self.winfo_x()+dx
        y = self.winfo_y()+dy
        self.geometry(f"+{x}+{y}")
    
    def _stop_move(self,e:object) -> None: # 停止移动窗体
        self.window_x = None
        self.window_y = None

    def Config(self,disabled_animation:bool=None,delay:int=None) -> None:
        if type(disabled_animation)!=NoneType:
            self.delay = 0 if disabled_animation else delay
        if delay:
            self.anidelay = delay

    @property
    def width(self) -> int:
        return self.winfo_width()
    
    @property
    def height(self) -> int:
        return self.winfo_height()
    
    def _frame_on_show(self,**kw) -> None:
        try:
            self.now_show.on_show()
        except:
            pass

    def show(self,name:object,mode:Literal['ls','rs','lf','rf','us','ds','uf','df','no']='ls',**show_kwargs) -> None:
        '''
        ```
        mode = {
            'ls': 'left_slow',
            'rs': 'right_slow',
            'lf': 'left_fast',
            'rf': 'right_fast',
            'us': 'up_slow',
            'ds': 'down_slow',
            'uf': 'up_fast',
            'df': 'down_fast',
            'no': None
        }
        ```
        ''' # FMCL让我学废了tkinter的“动画” （
        if self.running or self.now_show == name:
            print('running')
            return
        else:
            self.running = True
            self.forget_all()
            if name not in self.Frame:
                raise KeyError('frame "%s" not found'%name)
            width = self.width
            headheight = self.head.height
            y = headheight+1
            mv = 20
            now:Union[Frame,None] = None
            if mode != 'no' and self.now_show:
                now = self.now_show
                now.place(x=0,y=y)
            Case = Match(mode)
            def _end() -> None:
                "动画结束后调用的函数"
                self.running = False
                self.Frame[name].place_forget()
                if now:now.place_forget()
                self.Frame[name].place(x=0,y=y)
                self.now_show = self.Frame[name]
                self._frame_on_show(**show_kwargs)
            #region 动画部分
            if Case('ls'): # 慢速左移 [now|frame <-] OK
                now:Frame # NOTE 这是给IDE看的
                now.place(x=0,y=y)
                self.Frame[name].place(x=width,y=y)
                s = width # frame: x: width -> 0
                s2 = int(s*0.40)
                s1 = int(s*0.25)
                s0 = int(s*0.15)
                mv2 = int(mv*0.40)
                mv1 = int(mv*0.25)
                mv0 = int(mv*0.05) or 1
                def _show():
                    self.update()
                    x = self.Frame[name].winfo_x() # width -> 0
                    if x >= s2:
                        d = mv
                    elif x >= s1:
                        d = mv2
                    elif x >= s0:
                        d = mv1
                    elif x > 0:
                        d = mv0
                    else:
                        _end()
                        return
                    now.place(x=now.winfo_x()-d,y=y)
                    self.Frame[name].place(x=x-d,y=y)
                    self.after(self.anidelay,_show)
                _show()
            if Case('rs'): # 慢速右移 [frame|now ->] OK
                now:Frame
                now.place(x=0,y=y) # frame: x: -width -> 0
                self.Frame[name].place(x=-width,y=y)
                s = -width
                s2 = int(s*0.40)
                s1 = int(s*0.25)
                s0 = int(s*0.15)
                mv2 = int(mv*0.40)
                mv1 = int(mv*0.25)
                mv0 = int(mv*0.05) or 1
                def _show():
                    self.update()
                    x = self.Frame[name].winfo_x() # width -> 0
                    if x <= s2:
                        d = mv
                    elif x <= s1:
                        d = mv2
                    elif x <= s0:
                        d = mv1
                    elif x < 0: # 修了两个小时才发现这有个BUG...
                        d = mv0
                    else:
                        _end()
                        return
                    now.place(x=now.winfo_x()+d,y=y)
                    self.Frame[name].place(x=x+d,y=y)
                    self.after(self.anidelay,_show)
                _show()
            if Case('lf'): # 快速左移 [now|frame <-] OK
                now:Frame
                now.place(x=0,y=y)
                self.Frame[name].place(x=width,y=y)
                def _show():
                    self.update()
                    if self.Frame[name].winfo_x() >= 0: # width -> 0
                        now.place(x=now.winfo_x()-mv,y=y)
                        self.Frame[name].place(x=self.Frame[name].winfo_x()-mv,y=y)
                        self.after(self.anidelay,_show)
                    else:
                        _end()
                _show()
            if Case('rf'): # 快速右移 [frame|now ->] OK
                now:Frame
                now.place(x=0,y=y)
                self.Frame[name].place(x=-width,y=y)
                def _show() -> None:
                    self.update()
                    if now.winfo_x() < width:
                        now.place(x=now.winfo_x()+mv,y=y)
                        self.Frame[name].place(x=self.Frame[name].winfo_x()+mv,y=y)
                        self.after(self.anidelay,_show)
                    else:
                        _end()
                _show()
            if Case('us'): # 慢速上移 [now/frame ^^]
                #print('us') # y: height -> y; mv frame
                now:Frame
                height = self.height
                now.place(x=0,y=y)
                self.Frame[name].place(x=0,y=height)
                s = height+y
                s2 = int(s*0.50)
                s1 = int(s*0.25)
                s0 = int(s*0.10)
                mv2 = int(mv*0.40)
                mv1 = int(mv*0.25)
                mv0 = int(mv*0.05) or 1
                def _show() -> None:
                    self.update()
                    Y = self.Frame[name].winfo_y() - y
                    if Y >= s2:
                        d = mv
                    elif Y >= s1:
                        d = mv2
                    elif Y >= s0:
                        d = mv1
                    elif Y >= 0:
                        d = mv0
                    else:
                        _end()
                        return
                    self.Frame[name].place(x=0,y=self.Frame[name].winfo_y()-d)
                    self.after(self.anidelay,_show)
                _show()
            if Case('ds'): # 慢速下移 [frame/now __] 
                #print('ds') # 0 -> height; mv now
                now:Frame
                height = self.height
                s = height
                s2 = int(s*0.50)
                s1 = int(s*0.25)
                s0 = int(s*0.10)
                mv2 = int(mv*0.40)
                mv1 = int(mv*0.25)
                mv0 = int(mv*0.05) or 1
                height = self.height
                self.Frame[name].place(x=0,y=y)
                now.place(x=0,y=y)
                self.update()
                #print(...,now.winfo_y())
                def _show() -> None:
                    self.update()
                    Y = height-now.winfo_y() # ??? 不知怎么的就正常跑起来了……
                    if Y >= s2:
                        d = mv
                    elif Y >= s1:
                        d = mv2
                    elif Y >= s0:
                        d = mv1
                    elif Y > 0:
                        d = mv0
                    else:
                        _end()
                        return
                    now.place(x=0,y=now.winfo_y()+d)
                    self.after(self.anidelay,_show)
                _show()
            if Case('uf'): # 快速上移 [now/frame ^^]
                #print('uf')
                now:Frame
                height = self.height
                now.place(x=0,y=y)
                self.Frame[name].place(x=0,y=height)
                def _show() -> None:
                    self.update()
                    if self.Frame[name].winfo_y() > y:
                        self.Frame[name].place(x=0,y=self.Frame[name].winfo_y()-mv)
                        self.after(self.anidelay,_show)
                    else:
                        _end()
                _show()
            if Case('df'): # 快速下移 [frame/now __]
                #print('df')
                now:Frame
                height = self.height
                self.Frame[name].place(x=0,y=y)
                now.place(x=0,y=y)
                def _show() -> None:
                    self.update()
                    if now.winfo_y() < height:
                        now.place(x=0,y=now.winfo_y()+mv)
                        self.after(self.anidelay,_show)
                    else:
                        _end()
                _show()
            if Case('no'): # 直接显示 [frame]
                #print('no')
                _end()
            if Case.Else():
                raise ValueError("Unknow mode: %s"%mode)       
            #endregion

    def forget_all(self) -> None:
        for f in self.Frame:
            self.Frame[f].place_forget()
    
    def get_focus(self) -> None:
        self.attributes('-topmost',True)
        self.focus_force()
        self.after(100,lambda:self.attributes('-topmost',False))
        self.focus_force()
        self.focus_set()

    def _get_windows_icon(self) -> None:
        sub = Toplevel(self)
        sub.resizable(True,True)
        sub.geometry("20x20")
        sub.overrideredirect(True)
        sub.attributes('-topmost',True)
        self.after(200,lambda:(sub.focus_force(),sub.destroy()))
        self.get_focus()
        self.get_focus()

    def show_mainwindow(self) -> None:
        "让MainWindow逐渐显示"
        self.attributes('-alpha',0)
        self.smw_n = 0
        def _a():
            if self.smw_n < self.window_transp:
                self.smw_n += 0.08
                self.attributes('-alpha',self.smw_n)
                self.after(10,_a)
                #print(self.smw_n)
            else:
                return
        self.after(4,_a)

    def start(self) -> None:
        self.get_focus()
        self.after(16,self._get_windows_icon)
        self.after(64,self._get_windows_icon)
        def si():
            if self._index_frame:
                self.show(self._index_frame,'us')
        self.show_mainwindow()
        self.after(64,si)
        # mainloop调试
        #while True: 
        #    try:
        #        self.update()
        #    except:
        #        break
        self.mainloop()
    
    def add_frame(self,*frame_objs:object) -> None:
        for frame_obj in frame_objs:
            self.Frame[frame_obj] = frame_obj(self)

class WindowHead(Frame):
    "窗体页头"
    def __init__(self,parent:MainWindow) -> None:
        super().__init__(parent)
        self._parent = parent
        self.bg  = parent.color.bg0
        self.bg1 = parent.color.bg1
        self.bg2 = parent.color.bg2
        self.Canvas = Canvas(self,width=parent.width,height=45,bg=self.bg)
        self.Canvas.pack(fill=BOTH,expand=1) # 填充
        self.fn1 = lambda e:(parent._start_move(e),self.Canvas.config(bg=self.bg2),None)[-1] # 使得lambda返回None
        self.fn2 = lambda e:(parent._stop_move(e ),self.Canvas.config(bg=self.bg1),None)[-1]
        self.fn3 = lambda _:(self.Canvas.config(bg=self.bg1),None)[-1]
        self.fn4 = lambda _:(self.Canvas.config(bg=self.bg ),None)[-1]
        self.Canvas.bind(Binds.ButtonPress1,  self.fn1) # 按键按下
        self.Canvas.bind(Binds.ButtonRelease1,self.fn2) # 按键释放
        self.Canvas.bind("<B1-Motion>",parent._do_move) # 移动窗体
        self.Canvas.bind(Binds.Enter,self.fn3)
        self.Canvas.bind(Binds.Leave,self.fn4)
        bbg = (rgb(self.bg1)+rgb('#0A0A0A')).format_hex()
        self.destroy_window_button = MyButton(self,text='X',width=20,height=21,bg=bbg,bg1='#ff0000',bg2='#ee0000',command=lambda:(parent.window_close_command())) # 不使用lambda导致报错
        self.destroy_window_button.place(x=760,y=10)

    @property
    def width(self) -> int:
        self._parent.update()
        return self.winfo_width()

    @property
    def height(self) -> int:
        self._parent.update()
        return self.winfo_height()
    
    def color_config(self,bg:str=None,bg1:str=None,bg2:str=None) -> None:
        self.bg,self.bg1,self.bg2 = bg or self.bg,bg1 or self.bg1,bg2 or self.bg2
        self.config(bg=self.bg)
        

class _HintBox(Label):
    "一次性提示框（不直接调用）"
    def __init__(self,master:Widget,text:str,bg:str='#0000FF',fg:str='#FFFFFF',y=0,sleep:int=2560,exit_command:object=None,autoshow:bool=True) -> None:
        '''
        :master: 窗体
        :text: 文本
        :bg: 背景
        :fg: 字体颜色
        :y: Y轴坐标
        :sleep: 提示显示后的等待时间
        :exit_command: 显示完成后调用的函数
        :autoshow: 自动调用显示方法
        '''
        if bg == 'info':
            bg = '#119ce1'
        elif bg == 'warn':
            bg = '#ff8800'
        elif bg == 'error':
            bg = '#ff0000'
        self.master = master
        super().__init__(master,text=text,bg=bg,fg=fg)
        self.tkraise() # 置顶
        self.text = text
        self.y = y
        self.sleep = sleep
        self.ec = exit_command
        if autoshow:self.show()

    def _get_width(self) -> int:
        self.master.update()
        return self.winfo_width()

    def show(self) -> None:
        self.place(x=-100,y=self.y)
        self.w = self._get_width()
        self.wid = 0-self.w
        self.s = 3
        self.place(x=self.wid,y=0)
        def _show() -> None:
            self.place_forget()
            self.wid += self.s
            self.place(x=self.wid,y=self.y)
            if self.wid < 0:
                self.after(2,_show)
            else:
                self.place(x=0,y=self.y)
                self.after(self.sleep,self.hide)
        _show()

    def hide(self) -> None:
        self.w = self._get_width()
        self.wid = 0
        self.s = 3
        def _hide() -> None:
            self.place_forget()
            self.wid -= self.s
            self.place(x=self.wid,y=self.y)
            if self.wid > -self.w:
                self.after(2, _hide)
            else:
                if self.ec:
                    self.ec()
                self.destroy()
        _hide()

class HintBox:
    _showings:List[_HintBox] = []

    def _thread() -> None:
        last = None
        while True:
            sleep(0.1)
            if HintBox._showings:
                last = HintBox._showings[0]
                last.show()
                while True:
                    sleep(0.1)
                    if HintBox._showings:
                        if last != HintBox._showings[0]:
                            break
                    else:
                        break
    
    def _show(master:Widget,text:str,__c:str) -> None:
        if HintBox._showings:
            if HintBox._showings[0].text != text:
                HintBox._showings.append(_HintBox(master,text,__c,exit_command=lambda:(HintBox._showings.pop(0),None)[-1],y=20,autoshow=False))
        else:
            HintBox._showings.append(_HintBox(master,text,__c,exit_command=lambda:(HintBox._showings.pop(0),None)[-1],y=20,autoshow=False))

    def start_thread() -> None:
        "线程，启动！！（"
        Thread(target=HintBox._thread,daemon=True).start()
    
    def __init__(self,master:Widget) -> None:
        "master: 窗体"
        self.master = master
        HintBox.start_thread()

    def info(self,text:str) -> None:
        HintBox._show(self.master,text,'info')

    def warn(self,text:str) -> None:
        HintBox._show(self.master,text,'warn')

    def error(self,text:str) -> None:
        HintBox._show(self.master,text,'error')

class MyButton(Button):
    def __init__(self,master:WindowType,text:str='',width:int=100,height:int=20,command:Union[Function,None]=None,fg:str='#ffffff',fg1='#eeeeee',fg2='#bbbbbb',bg:str='#0084d0',bg1:str='#23a8f2',bg2:str='#1f7caf',bg3:str='#8bd5ff',image:PhotoImage=None,state:str=NORMAL) -> None:
        self.image = image or PhotoImage(width=0,height=0)
        super().__init__(master,text=text,width=width,height=height,command=command,fg=fg,activeforeground=fg1,disabledforeground=fg2,bg=bg,activebackground=bg2,image=self.image,bd=0,compound=CENTER,state=state,cursor=MouseCursor.hand2 if state != DISABLED else MouseCursor.no)
        self.text = text
        self.width = width
        self.height = height
        self.state = state
        self.command = command
        self.fg = fg
        self.fg1 = fg1
        self.fg2 = fg2
        self.bg = bg
        self.bg1 = bg1 
        self.bg2 = bg2
        self.bg3 = bg3
        self.bind(Binds.Enter,self.mouse_enter)
        self.bind(Binds.Leave,self.mouse_leave)
        if state == DISABLED:
            self.config(bg=self.bg3)

    def my_config(self,text:str=None,width:int=None,height:int=None,command:Union[Function,None]=None,fg:str=None,fg1:str=None,fg2:str=None,bg:str=None,bg1:str=None,bg2:str=None,bg3:str=None,image:PhotoImage=None,state:str=None) -> None:
        self.config(text=text or self.text);self.text=text or self.text
        self.config(width=width or self.width);self.width=width or self.width
        self.config(height=height or self.height);self.height=height or self.height
        self.config(command=command or self.command);self.command=command or self.command
        self.config(fg=fg or self.fg);self.fg=fg or self.fg
        self.config(activeforeground=fg1 or self.fg1);self.fg1 = fg1 or self.fg1
        self.config(disabledforeground=fg2 or self.fg2);self.fg2 = fg2 or self.fg2
        self.config(bg=bg or self.bg);self.bg=bg or self.bg
        self.bg3 = bg3 or self.bg3
        self.bg1 = bg1 or self.bg1
        self.config(activebackground=bg2 or self.bg2)
        self.bg2 = bg2 or self.bg2
        self.config(image=image or self.image)
        self.image = image or self.image
        if state:
            if state == DISABLED:
                self.config(state=DISABLED,bg=self.bg3,cursor=MouseCursor.no)
            else:
                self.config(state=state,bg=self.bg,cursor=MouseCursor.hand2)
            self.state = state

    def mouse_enter(self,e:Event) -> None:
        if self.state != DISABLED:
            self.config(bg=self.bg1)
    
    def mouse_leave(self,e:Event) -> None:
        if self.state != DISABLED:
            self.config(bg=self.bg)

    def destroy(self) -> None:
        self.unbind(Binds.Enter)
        self.unbind(Binds.Leave)
        return super().destroy()

class MyMsgbox(Tooltip):
    def __init__(self,mainwindow:MainWindow,title:str,text:str,*buttons:str) -> int:
        super().__init__(mainwindow)
        self.mw = mainwindow
        self.title = title
        self.text = text
        self.buttons = [str(b) for b in buttons]
        if len(self.buttons) > 3 or len(self.buttons) < 1:
            raise ValueError("按键长度错误")

    def show(self) -> None:
        ...

class MyMsgboxFrame(Frame):
    def __init__(self,parent:MainWindow) -> None:
        super().__init__(self,parent)
        height = parent.height - parent.head.height
        self.canvas = Canvas(self,width=800,height=height,background=...)

class MyEntry(Entry):
    def __init__(self,master=None,placeholder="PLACEHOLDER",fg0:str='#000000',fg1:str='#999999'):
        super().__init__(master,fg=fg0,bd=1,relief='solid')
        self.default_color = fg1
        self.original_color = self.cget("fg")
        self.set_placeholder(placeholder)
        self.binds0 = self.bind(Binds.FocusIn,self.on_entry_click)
        self.binds1 = self.bind(Binds.FocusOut,self.on_focusout)

    def set_text(self,text) -> None:
        self.delete(0,"end")
        self.insert(0,text)

    def set_placeholder(self,placeholder) -> None:
        self.default_text = placeholder
        self.set_text(placeholder)
        self['fg'] = self.default_color
        
    def on_entry_click(self,e=0) -> None:
        if self['fg'] == self.default_color:
            self.delete(0,"end") 
            self['fg'] = self.original_color

    def on_focusout(self,e=0) -> None:
        if not self.get():
            self.set_placeholder(self.default_text)
            self['fg'] = self.default_color

    def get_text(self):
        if self['fg'] == self.default_color:
            return ''
        else:
            return self.get()
        
    def destroy(self) -> None:
        self.unbind(Binds.FocusIn,self.binds0)
        self.unbind(Binds.FocusOut,self.binds1)
        super().destroy()

class NoneFrame(Frame):
    def __init__(self,master) -> None:
        super().__init__(master)
    def on_show(self) -> None:
        pass

class TestFrame1(Frame): # 测试MainWindow用页面 1
    def __init__(self,parent:MainWindow) -> None:
        super().__init__(parent)
        Label(self,text='测试页面1').pack()
        Label(self,text="e……这个版本……能交互的只有这些……").pack()
        fn = lambda:mb.my_config(state=DISABLED)
        fn1 = lambda:mb.my_config(state=NORMAL)
        fn2 = lambda:parent.show(TestFrame2,'us')
        mb = MyButton(self,text='disabled',width=220,height=32,command=fn)
        mb.pack()
        b = MyButton(self,text='enabled',width=200,height=20,command=fn1,state=NORMAL)
        b.pack()
        Tooltip(mb,"看什么看？没见过button啊？（")
        Tooltip(b,'114514')
        MyButton(self,text='翻页',width=200,height=20,command=fn2).pack()
        Combobox(self).pack()
        Radiobutton(self).pack()
        MyEntry(self,).pack()
        s = ScrollableFrame(self,width=400,height=230)
        for i in range(200):
            s.add_widget(MyButton(s(),text='114514-%d'%i))
        s.pack()
        
    def on_show(self) -> None:
        pass

class TestFrame2(Frame): # 测试MainWindow用页面 2
    def __init__(self,parent:MainWindow) -> None:
        super().__init__(parent)
        Label(self,text='测试页2').pack()
        Label(self,text="当前版本：dev 0.0.0").pack()
        Label(self,text="亻尔 女子").pack()
        Label(self,text="什么？！你竟然……成功翻页了？！\n虽然这是你的一小步，但却是mc-124咕咕咕事业的一大步（").pack()
        Label(self,text="翻页也算是种能玩的吧……？").pack()
        MyButton(self,text='翻 yee',width=220,command=lambda:parent.show(TestFrame1,'ds')).pack()
        Canvas(self,width=400,height=300).pack()
    def on_show(self) -> None:
        pass
# system-min-window-size: 800x600/1024x768; window-size: minecraft-default_854x480 pcl2-default_860x520
    

def test():
    def close():
        mw.destroy()
    mw = MainWindow(geometry='800x500',title='Simple-Craft-Launcher [dev 0.0.0]',index_frame=TestFrame1,delay=3,window_close_command=close) # 确定了默认窗口大小是800x500
    mw.add_frame(TestFrame1,TestFrame2)
    mw.start()

if __name__ == "__main__":
    test()