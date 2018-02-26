import tornado.ioloop
import tornado.web
import os
from Lib.Database.Mysql import ConnectionPool
# # # from Lib.Jobs import Jobs
from Lib.Socket import Socket
from Lib.Core import Config
from Lib.Core import GlobalManager
from Lib.Core.Container import Container
from Lib.Log import Log
from Lib.Cache import Cache
from Lib.Http.StaticFileHandler import StaticFileHandler
from Lib.Http.Routing.ControllerDispatcher import ControllerDispatcher
from Lib.Http.Routing.Router import Router
from Http.Route import Route


class Application(Container):

    def boot(self):
        GlobalManager.init()
        GlobalManager.set('app', self)
        root = os.path.dirname(__file__)
        GlobalManager.set('root', root)

        Config.load()
        self.singleton('Config', Config)
        self.singleton('ConnectionPool', lambda app: ConnectionPool(app.make('Config').get('DB')))
        GlobalManager.set('ConnectionPool', self.make('ConnectionPool'))

        self.instance('Router', Router())
        self.singleton('Route', lambda app: Route(app.make('Router')))
        self.singleton('Log', lambda app: Log(app.make('Config').get('Log')))

        self.singleton('Cache', lambda app: Cache(app.make('Config').get('Cache')))

        webServerConfig = self.make('Config').get('WebServer')
        application = tornado.web.Application([
            (r"/css/(.*)", StaticFileHandler, dict(path='Build/css')),
            (r"/js/(.*)", StaticFileHandler, dict(path='Build/js')),
            (r"/static/(.*)", StaticFileHandler, dict(path=os.path.join(root, 'Storage/JavBus'))),
            (r"/socket", Socket, dict(app=self)),
            (r"/(.*?)", ControllerDispatcher, dict(app=self)),
            # # (r"/setting/(\w*?)", SettingHandler, dict(pool=pool)),
            # # (r"/getData/(\w*?)", GetDataHandler, dict(pool=pool)),
            # (r"/(.*?)", Controller),
            # (r"/(.*?)", tornado.web.StaticFileHandler, dict(path='Build', default_filename="index.html")),
        ], **webServerConfig)
        application.listen(webServerConfig['listen'])
        tornado.ioloop.IOLoop.instance().start()
