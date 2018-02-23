import tornado.web


class StaticFileHandler(tornado.web.StaticFileHandler):

    def write_error(self, status_code, **kwargs):
        self.write("404 Not Found")
