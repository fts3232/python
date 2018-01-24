import tornado.ioloop
import tornado.web
import sys
from Handler.GetDataHandler import GetDataHandler
from Handler.GetTagHandler import GetTagHandler
from Handler.SocketHandler import SocketHandler
sys.path.append("../")
from Mysql import ConnectionPool


config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'JavBus',
    'charset': 'utf8',
    'max_connection': 20,
    'min_connection': 2,
}
pool = ConnectionPool(config)

settings = {
    'template_path': 'Build',
    'static_path': '../JavBus',
    'static_url_prefix': '/static/',
    'debug': True
}

application = tornado.web.Application([
    (r"/getData", GetDataHandler, dict(pool=pool)),
    (r"/getTag", GetTagHandler, dict(pool=pool)),
    (r"/socket", SocketHandler, dict(pool=pool)),
    (r"/(.*?)", tornado.web.StaticFileHandler, dict(path='Build', default_filename="index.html")),
    # (r"/css/(.*)", tornado.web.StaticFileHandler, dict(path='Build/css')),
    # (r"/js/(.*)", tornado.web.StaticFileHandler, dict(path='Build/js')),
], **settings)


application.listen(8000)
tornado.ioloop.IOLoop.instance().start()
