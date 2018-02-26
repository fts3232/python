import os
from Lib.Core import GlobalManager


config = {
    'roots': ['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads'],
    'suffix': ['.avi', '.mp4'],
    'storage_path': os.path.join(GlobalManager.get('root'), 'Storage/JavBus/Movie')
}
