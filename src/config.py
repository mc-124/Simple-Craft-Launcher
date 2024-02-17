#try:
#    from secrecy import sys_key,read_regedit,crypto_key,idr,idp
#except ModuleNotFoundError:
#    def sys_key():...
#    def read_regedit():...
#
#from utils import regedit,SCL_NAME
#from winreg import REG_SZ
#
#
#def update_regedit() -> None:
#    if not regedit.exists(SCL_NAME,"WindowsId"):regedit.write(SCL_NAME,"WindowsId",REG_SZ,idp().replace('-',''))
#    if not regedit.exists(SCL_NAME,"SystemId"):regedit.write(SCL_NAME,"SystemId",REG_SZ,idr())
#    if regedit.type(SCL_NAME,"WindowsId") != 1 or regedit.type(SCL_NAME,"SystemId") != 1:
#        regedit.write(SCL_NAME,"WindowsId",REG_SZ,idp().replace('-',''))
#        regedit.write(SCL_NAME,"SystemId",REG_SZ,idr())
#
#
#
#
#if __name__ == "__main__":
#    0
#
#
#
#def get_language() -> str:
#    return 'zh-CN'
