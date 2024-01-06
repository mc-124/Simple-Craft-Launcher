- zh-CN
## Simple-Craft-Launcher
Minecraft Launcher 

![version](https://img.shields.io/badge/release-None-green)
![version](https://img.shields.io/badge/snapshot-None-yellow)
![version](https://img.shields.io/badge/dev-0.0.1-red)
![core](https://img.shields.io/badge/Core-0.0.1-green)
![gui](https://img.shields.io/badge/GUI-0.0.1-green)

> - 支持微软登录
> - 支持外置皮肤站登录（authlib-injector）
> - 支持离线登录
> - 可安装Minecraft JE Client
> - 可安装Minecraft JE Server
> - 可安装Mods（支持中文搜索）
> - 支持多语言
> - 自带运行时，无需另外安装运行时
> - MIT开源（除了部分加密逻辑与CurseForgeApiKey外）
> - 完全免费
> - 多线程下载
> - 自动安装Java

### UI库
> ![Tk/Tcl](https://img.shields.io/badge/Tk%20Tcl-8.6-red)

### 部分缺点
> 未知

### 进度
> | 名称 | 进度 |
> |:------|:------|
> | 创建项目并完善底层函数 | 进行中 99% |
> | Minecraft启动核心 | 等待 3% |
> | tkinter GUI | 进行中 25% |
> | 完善UI动画 | 进行中 5% |
> | MC启动模块 | 进行中 1% |
> | MC登录模块 | 进行中 50% |
> | 加载器安装模块 | 等待 1% |
> | Mod下载模块 | 进行中 50% |
> | 绑定UI | 等待 1% |
> | 完善项目 | 等待 0% |
> | 完善Github仓库 | 等待 0% |
> | 支持Linux | 等待 20% |
> | 支持OSX | 等待 0% |

### 计划支持的操作系统与架构
> | 系统/架构 | Windows | Linux | MacOS |
> | :----- | :-----  | :----- | :----- |
> | x86_64 | ☑️ | ☑️ | ![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png) |
> | x86 | ☑️ | ☑️ | ❎ |
> | Arm64 | ![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png) | ![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png) | ![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png) |
> - "☑️":支持
> - "❎":不支持
> - "⚠️":部分功能异常
> - \"![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)\":暂无可执行文件
#### 注：
> - Windows仅支持Windows7及更高版本（不包括WindowsServer2008）
> - MacOS仅支持OSX，跨架构靠系统自身
> - Linux仅在Ubuntu18.04-AMD64测试并进行优化，仅支持Ubuntu18.04及更高版本
> - 仅支持Python3.7，暂不支持其他版本的Python解释器（包括更高版本的）

### 编程语言
> <a href="https://www.python.org/downloads/release/python-379/"><img src="https://img.shields.io/badge/Python_3.7.9_x86-3d7aab?style=for-the-badge&logo=python&logoColor=ffffff" alt="Python3.7.9"></a>
> <a href="https://www.python.org/downloads/release/python-375/"><img src="https://img.shields.io/badge/Python_3.7.5_x64-3d7aab?style=for-the-badge&logo=python&logoColor=ffffff" alt="Python3.7.5"></a>

### 使用的所有第三方库
> | 名称 | 对库的更改 |
> | :-----: | :-----: |
> | ![pyaudio](https://img.shields.io/badge/pyaudio-0.2.13-green) | 无改动 |
> | ![bs4](https://img.shields.io/badge/BeautifulSoup4-4.12.2-green) | 删去了test |
> | ![psutil](https://img.shields.io/badge/psutil-5.9.5-green) | 稍作更改 |
> | ![cryptodome](https://img.shields.io/badge/PyCryptoDome-3.19.0-green) | 删去大量用不到的部分 |

### 打包工具
> ![Nuitka](https://img.shields.io/badge/Nuitka-1.9.6-green)
> ![MSVC2019](https://img.shields.io/badge/MSVC_2019_x86-14.29.30133-green)
> ![GCC7](http://img.shields.io/badge/GCC-7-green)
