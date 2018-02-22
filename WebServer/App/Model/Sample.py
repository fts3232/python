from . import Model


class Sample(Model):

    def get(self, movie_id):
        return self._db.select('select URL from SAMPLE where MOVIE_ID = :MOVIE_ID', {'MOVIE_ID': movie_id})
