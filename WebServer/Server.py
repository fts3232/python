import tornado.ioloop
import tornado.web
import sys
import os
sys.path.append("./App")
from Handler.GetDataHandler import GetDataHandler
from Handler.SocketHandler import SocketHandler
from Handler.SettingHandler import SettingHandler
from Lib.Mysql import ConnectionPool
# from Lib.Jobs import Jobs
from Config.DB import config
import sys
sys.path.append(os.path.join(os.getcwd(), 'App'))

# Jobs().run()

pool = ConnectionPool(config)

settings = {
    'cookie_secret': 'S6Bp2cVjSAGFXDZqyOh+hfn/fpBnaEzFh22IVmCsVJQ=',
    'xsrf_cookies': True,
    'template_path': 'Build',
    'static_path': './Storage/JavBus',
    'static_url_prefix': '/static/',
    'debug': True
}

application = tornado.web.Application([
    (r"/socket", SocketHandler, dict(pool=pool)),
    (r"/setting/(\w*?)", SettingHandler, dict(pool=pool)),
    (r"/getData/(\w*?)", GetDataHandler, dict(pool=pool)),
    (r"/(.*?)", tornado.web.StaticFileHandler, dict(path='Build', default_filename="index.html")),
    # (r"/css/(.*)", tornado.web.StaticFileHandler, dict(path='Build/css')),
    # (r"/js/(.*)", tornado.web.StaticFileHandler, dict(path='Build/js')),
], **settings)


application.listen(8000)
tornado.ioloop.IOLoop.instance().start()
