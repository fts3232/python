class Tag():
    __db = None

    def __init__(self, db):
        self.__db = db

    def get(self, tag):
        return self.__db.select('select TAG_ID,TAG_NAME from TAG where TAG_ID IN({tag})'.format(tag=tag))

    def getAll(self):
        return self.__db.select('select TAG_ID,TAG_NAME from TAG')
