#from Core.Utils.net import requests
import subprocess
from os import remove
from os.path import isfile
from . import (
    AUTHLIB_INJECTOR,
    SIMPLE_BROWSER,
    SIMPLE_BROWSER_LOG
)

class OauthCode(str):...

MICROSOFT_AUTHSERVER = "https://authserver.mojang.com/"
MICROSOFT_OAUTH = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf"
# return url       https://login.live.com/oauth20_desktop.srf?code=M.C106_SN1.2.50634a11-3804-3f00-6a63-ec9d737d4d84&lc=2052
#                  ===================忽略=====================-----------------------目标---------------------------==忽略==

def oauth_login() -> OauthCode:
    if isfile(SIMPLE_BROWSER):
        subprocess.call([SIMPLE_BROWSER,f'--default-url={MICROSOFT_OAUTH}'])


if __name__ == "__main__":
    print(oauth_login())
    
 
    