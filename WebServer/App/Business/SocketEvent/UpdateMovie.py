from Business.JavBus import JavBus


class UpdateMovie():
    __options = None

    def __init__(self, options=None):
        self.__options = options

    def run(self):
        pool = self.__options['app'].make('ConnectionPool')
        JavBus(pool).updateMovie(self.__options['data']['movie_id'], self.__options['data']['identifier'])
        self.__options['print']('updateMovie', '修改成功')
