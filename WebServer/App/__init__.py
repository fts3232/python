import Config
import tornado.ioloop
import tornado.web
from Lib.Mysql import ConnectionPool
# # # from Lib.Jobs import Jobs
from Container import Container
from Http.Router import Router


class Application(Container):

    def boot(self):
        self.singleton('Config', Config)
        self.singleton('ConnectionPool', lambda app: ConnectionPool(app.make('Config').DB))
        application = tornado.web.Application([
            (r"/css/(.*)", tornado.web.StaticFileHandler, dict(path='Build/css')),
            (r"/js/(.*)", tornado.web.StaticFileHandler, dict(path='Build/js')),
            (r"/(.*?)", Router, dict(app=self)),
            # # (r"/setting/(\w*?)", SettingHandler, dict(pool=pool)),
            # # (r"/getData/(\w*?)", GetDataHandler, dict(pool=pool)),
            # (r"/(.*?)", Controller),
            # (r"/(.*?)", tornado.web.StaticFileHandler, dict(path='Build', default_filename="index.html")),
        ], **self.make('Config').WebServer)
        application.listen(self.make('Config').WebServer['listen'])
        tornado.ioloop.IOLoop.instance().start()
