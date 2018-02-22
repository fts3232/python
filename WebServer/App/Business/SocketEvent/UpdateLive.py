from Business.Live import Live


class UpdateLive():
    __options = None

    def __init__(self, options=None):
        self.__options = options

    def run(self):
        Live().run()
        self.__options['print']('updateLive')
