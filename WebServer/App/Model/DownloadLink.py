from . import Model


class DownloadLink(Model):

    def get(self, movie_id):
        return self._db.select('select LINK,PUBLISH_TIME from DOWNLOAD_LINK where MOVIE_ID = :MOVIE_ID', {'MOVIE_ID': movie_id})
