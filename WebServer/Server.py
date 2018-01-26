import tornado.ioloop
import tornado.web
import sys
sys.path.append("./App")
from Handler.GetDataHandler import GetDataHandler
from Handler.GetTagHandler import GetTagHandler
from Handler.SocketHandler import SocketHandler
from Handler.GetLiveHandler import GetLiveHandler
from Lib.Mysql import ConnectionPool
from Lib.Jobs import Jobs
from Config.DB import config


Jobs().run()

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
    (r"/getData", GetDataHandler, dict(pool=pool)),
    (r"/getTag", GetTagHandler, dict(pool=pool)),
    (r"/socket", SocketHandler, dict(pool=pool)),
    (r"/getLive", GetLiveHandler),
    (r"/(.*?)", tornado.web.StaticFileHandler, dict(path='Build', default_filename="index.html")),
    # (r"/css/(.*)", tornado.web.StaticFileHandler, dict(path='Build/css')),
    # (r"/js/(.*)", tornado.web.StaticFileHandler, dict(path='Build/js')),
], **settings)


application.listen(8000)
tornado.ioloop.IOLoop.instance().start()
