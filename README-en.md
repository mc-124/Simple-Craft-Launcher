- This program is under development, please do not download
- The complete source code will be uploaded once the project is completed.

- [zh-CN](https://github.com/mc-124/Simple-Craft-Launcher/blob/main/README.md)
- en-US
# Simple-Craft-Launcher
Minecraft Launcher 

> ![version](https://img.shields.io/badge/release-None-green)
> ![version](https://img.shields.io/badge/snapshot-None-yellow)
> ![version](https://img.shields.io/badge/dev-0.0.1-red)
> ![core](https://img.shields.io/badge/Core-0.0.1-green)
> ![gui](https://img.shields.io/badge/GUI-0.0.1-green)

> * Supports Microsoft login
> * Supports login with an external skin site (authlib-injector)
> * Supports offline login
> * Can install Minecraft JE Client
> * Can install Minecraft JE Server
> * Can install Mods (supports Chinese search)
> * Supports multiple languages
> * Comes with runtime, no need to install separately (but plugins are required: obligatory (ffmpeg), optional (built-in browser component))
> * Open-source with MIT license (except for some encryption functions and CurseForgeApiKey)
> * Completely free
> * Multi-threaded downloading
> * Auto-installs Java

### UI library
> ![Tk/Tcl](https://img.shields.io/badge/Tk%20Tcl-8.6-red)

### Some Disadvantages
> 1. tkinter ...

### Progress
> |Name|Progress|
> |-|-|
> |Project creation and completion of basic functions|Almost done 99%|
> |Minecraft core|In progress 15%|
> |tkinter GUI|Pause 35%|
> |Completing UI animations|Pause 60%|
> |Minecraft launch module|In progress 15%|
> |Minecraft login module|Waiting 50%|
> |Loader installation module|Waiting 5%|
> |Mod download module|Waiting 50%|
> |UI binding|Waiting 2%|
> |Project completion|Waiting 0%|
> |Github repository completion|Waiting 1%|
> |Linux support|Waiting 20%|
> |OSX support|Waiting 1%|

### Planned supported OS and architectures
> |System/Architecture|Windows|Linux|MacOS|
> |-|-|-|-|
> |x86_64|☑️|☑️|![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)|
> |x86|☑️|☑️|❎|
> |Arm64|![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)|![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)|![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)|
> - "☑️": supported
> - "❎": not supported
> - "⚠️": some features abnormal
> - /*![fwn](https://d.kstore.space/download/4904/SCL/website/fwn.png)\": executable file not available 
#### Note：
> Windows supports only from Windows7 and above (excluding WindowsServer2008)
> MacOS only supports OSX, cross-architecture relies on the system itself
> Linux was tested and optimized only for Ubuntu18.04-AMD64, supports only Ubuntu18.04 and above
> Supports only Python3.7, does not support other versions of Python interpreter (including higher versions)

### Programming languages
> |Platform|Programming language|
> |-|-|
> |Windows platform|
<a href="https://www.python.org/downloads/release/python-379/"><img src="https://img.shields.io/badge/Python_3.7.9_win32_x86-3d7aab?style=for-the-badge&logo=python&logoColor=ffffff" alt="Python3.7.9"></a>|
> |Linux platform|
<a href="https://www.python.org/downloads/release/python-375/"><img src="https://img.shields.io/badge/Python_3.7.5_linux_x64-3d7aab?style=for-the-badge&logo=python&logoColor=ffffff" alt="Python3.7.5"></a>|
> |MacOS platform|<a>Python3.7.?</a>|

### All third-party libraries used
> |Name|Changes to the library|
> |-|-|
> |![pyaudio](https://img.shields.io/badge/pyaudio-0.2.13-green)|No changes|
> |![bs4](https://img.shields.io/badge/BeautifulSoup4-4.12.2-green)|Test removed|
> |![psutil](https://img.shields.io/badge/psutil-5.9.5-green)| Minor changes|
> |![cryptodome](https://img.shields.io/badge/PyCryptoDome-3.19.0-green)| Removed many unused parts|

### Packaging tools
> ![Nuitka](https://img.shields.io/badge/Nuitka-1.9.6-green)
> ![GCC13](http://img.shields.io/badge/GCC_x86-13.2.0-green)
