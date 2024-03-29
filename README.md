* 2024.03.10 起暂停开发直到 2024.07.01

总进度：40%

- 此程序正在编写中，请勿下载
- 完整的源代码将在该项目完成后上传

- [en-US](https://github.com/mc-124/Simple-Craft-Launcher/blob/main/README.md)
- [en-US](https://github.com/mc-124/Simple-Craft-Launcher/blob/main/README-en.md) （更新较慢）
# Simple-Craft-Launcher
Minecraft Launcher 

> ![version](https://img.shields.io/badge/release-None-green)
> ![version](https://img.shields.io/badge/snapshot-None-yellow)
> ![version](https://img.shields.io/badge/dev-0.0.1-red)
> ![core](https://img.shields.io/badge/Core-0.0.1-green)
> ![gui](https://img.shields.io/badge/GUI-0.0.1-green)

> * 支持微软登录
> * 支持外置皮肤站登录（authlib-injector）
> * 支持离线登录
> * 可安装Minecraft JE Client
> * 可安装Minecraft JE Server
> * 可安装Mods（支持中文搜索）
> * 支持多语言
> * 自带运行时，无需另外安装运行时
> * MIT开源（除了部分加密函数与CurseForgeApiKey外）
> * 完全免费
> * 多线程下载
> * 自动安装Java

### UI库
> ![Tk/Tcl](https://img.shields.io/badge/Tk%20Tcl-8.6-red)

### 部分缺点
> 1.tkinter（

### 进度
> |名称|进度|
> |-|-|
> |创建项目并完善底层函数|基本完成 99%|
> |Minecraft核心|进行中 18%|
> |tkinter GUI|暂停 35%|
> |完善UI动画|暂停 60%|
> |MC启动模块|进行中 15%|
> |MC登录模块|等待 50%|
> |加载器安装模块|等待 5%|
> |Mod下载模块|进行中 60%|
> |绑定UI|等待 2%|
> |完善项目|等待 0%|
> |完善Github仓库|等待 1%|
> |支持Linux|等待 20%|
> |支持OSX|等待 1%|

### 计划支持的操作系统与架构
> |系统/架构|Windows|Linux|MacOS|
> |-|-|-|-|
> |x86_64|☑️|☑️|![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)|
> |x86|☑️|![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)|❎|
> |Arm64|![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)|![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)|![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)|
> - "☑️":支持
> - "❎":不支持
> - "⚠️":部分功能异常
> - \"![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)\":暂无可执行文件
#### 注：
> Windows仅支持Windows7及更高版本（不包括WindowsServer2008）（未来可能会出XP版）
> MacOS最低支持OSX，跨架构靠系统自身
> Linux仅在Ubuntu18.04-AMD64测试并进行优化，仅支持Ubuntu18.04及更高版本

### 编程语言
> |平台|编程语言|
> |-|-|
> |Windows平台|[![py379win32](https://img.shields.io/badge/Python_3.7.9_win32_x86-3d7aab?style=for-the-badge&logo=python&logoColor=ffffff)](https://www.python.org/downloads/release/python-379/)|
> |Linux平台|[![py375linux](https://img.shields.io/badge/Python_3.7.5_linux_x64-3d7aab?style=for-the-badge&logo=python&logoColor=ffffff)](https://www.python.org/downloads/release/python-375/)|
> |MacOS平台|[![py379osx](https://img.shields.io/badge/Python_3.7.9_osx_64bit-3d7aab?style=for-the-badge&logo=python&logoColor=ffffff)](https://www.python.org/downloads/release/python-379/)|

### 使用的所有第三方库
> |名称|对库的更改|
> |-|-|
> |![bs4](https://img.shields.io/badge/BeautifulSoup4-4.12.3-green)|删去了test|
> |![psutil](https://img.shields.io/badge/Psutil-5.9.8-green)|删去用不上的模块|
> |![zipfile36](https://img.shields.io/badge/Zipfile36-0.1.3-green)|无改动|
> |![pil](https://img.shields.io/badge/Pillow-9.5.0-green)|删去用不上的模块（2MB）|
> |![send2trash](https://img.shields.io/badge/Send2Trash-1.8.2-green)|无改动|
> |![toml](https://img.shields.io/badge/Toml-0.10.2-green)|无改动|
> |![typing_extensions](https://img.shields.io/badge/TypingExtensions-4.7.1-green)|无改动|

### 打包工具
> ![Nuitka](https://img.shields.io/badge/Nuitka-2.0.1-green)
> ![GCC13](https://img.shields.io/badge/GCC_x86-13.2.0-green)
