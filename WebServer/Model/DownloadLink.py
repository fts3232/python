class DownloadLink():
    __db = None

    def __init__(self, db):
        self.__db = db

    def get(self, movie_id):
        return self.__db.select('select LINK,PUBLISH_TIME from DOWNLOAD_LINK where MOVIE_ID = :MOVIE_ID', {'MOVIE_ID': movie_id})
