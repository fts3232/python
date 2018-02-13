from Business.Live import Live


class UpdateLive():
    __options = None

    def __init__(self, options=None):
        self.__options = options

    def run(self):
        obj = Live()
        obj.run()
        self.__options['print']('updateLive')
