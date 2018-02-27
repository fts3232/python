class Router():
    __router = {'get': {}, 'post': {}, 'put': {}, 'delete': {}}

    def __init__(self, route):
        route(self)

    def get(self, path, controller):
        self.bind('get', path, controller)

    def post(self, path, controller):
        self.bind('post', path, controller)

    def put(self, path, controller):
        self.bind('put', path, controller)

    def delete(self, path, controller):
        self.bind('delete', path, controller)

    def bind(self, method, path, controller):
        self.__router[method][path] = controller

    def list(self):
        return self.__router
