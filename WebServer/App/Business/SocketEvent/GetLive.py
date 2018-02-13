import pickle
import os


class GetLive():
    __options = None

    def __init__(self, options=None):
        self.__options = options

    def run(self):
        path = os.path.join(os.getcwd(), 'Storage/live.pkl')
        fo = open(path, 'rb+')
        ret = fo.read()
        live_list = pickle.loads(ret)
        for x in live_list:
            live_list[x] = sorted(live_list[x].items(), key=lambda item: item[1]['state'], reverse=True)
        self.__options['print']('getLive', live_list)
