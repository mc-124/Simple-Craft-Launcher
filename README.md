- zh-CN
## Simple-Craft-Launcher
Minecraft Launcher 

![version](https://img.shields.io/badge/release-None-green)
![version](https://img.shields.io/badge/snapshot-None-yellow)
![version](https://img.shields.io/badge/dev-0.0.1-red)
![core](https://img.shields.io/badge/Core-0.0.1-green)

- 支持正版登录
- 支持外置登录（authlib-injector）
- 支持离线登录
- 可安装Minecraft JE Client
- 可安装Minecraft JE Server
- 可安装Mods（支持中文搜索）
- 支持多语言
- 自带运行时，无需另外安装运行时
- MIT开源（除了部分加密逻辑与CurseForgeApiKey外）
- 完全免费
- 多线程下载
- 自动安装Java

### UI库
![Tk/Tcl](https://img.shields.io/badge/Tk%20Tcl-8.6-red)

### 部分缺点
- UI有点丑（为了让exe尽可能的小，所以使用的是Tk/Tcl 8.6）

### 进度
| 名称 | 进度 |
|:------:|:------:|
| 创建项目并完善底层函数 | 进行中 98% |
| Minecraft启动核心 | 等待 1% |
| UI | 进行中 10% |
| 完善UI动画 | 进行中 1% |
| MC启动模块 | 进行中 1% |
| MC登录模块 | 进行中 50% |
| 加载器安装模块 | 等待 0% |
| Mod下载模块 | 进行中 35% |
| 绑定UI | 等待 0% |
| 完善项目 | 等待 0% |
| 完善Github仓库 | 等待 0% |

### 计划支持的操作系统与架构
#### 支持的系统
| 名称 | 是否支持 |
| :-----: | :-----: |
| <= Windows Server 2008 | False |
| >= Windows 7 | True |
| Linux | False |
| MacOS | False |
| Other | False |
#### 支持的架构
| 名称 |
| :-----: |
| x86 |
| AMD64 |
| Inte64 |
| ARM 64 |

### 编程语言
![Python 3.7.9 x86](https://img.shields.io/badge/Python_3.7.9_x86-3d7aab?style=for-the-badge&logo=python&logoColor=ffffff)

### 使用的所有第三方库
| 名称 | 类型 | 重命名 |
| :-----: | :-----: | :-----: |
| ![plyer](https://img.shields.io/badge/plyer-2.1.0-green) | 删去了除windows外的api | 无重命名 |
| ![pyaudio](https://img.shields.io/badge/pyaudio-0.2.13-green) | 无改动 | 无重命名 |
| ![bs4](https://img.shields.io/badge/BeautifulSoup4-4.12.2-green) | 删去了test | 无重命名 |
| ![psutil](https://img.shields.io/badge/psutil-5.9.5-green) | 仅保留获取内存信息函数 | psutil_memory |
| ![tzlocal](https://img.shields.io/badge/tzlocal-5.1-green) | 无删改 | 无重命名 |
| ![cryptodome](https://img.shields.io/badge/PyCryptoDome-3.19.0-green) | 仅保留了AES加密算法 | AES_Crypto |

### 打包工具
![Nuitka](https://img.shields.io/badge/Nuitka-1.8.6-green)
![MSVC2019](https://img.shields.io/badge/MSVC_2019_x86-14.29.30133-green)
