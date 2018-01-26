class Star():
    __db = None

    def __init__(self, db):
        self.__db = db

    def get(self, star):
        return self.__db.select('select STAR_ID,STAR_NAME from STAR where STAR_ID IN({star})'.format(star=star))
