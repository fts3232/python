from . import Model


class Star(Model):

    def get(self, star):
        return self._db.select('select STAR_ID,STAR_NAME from STAR where STAR_ID IN({star})'.format(star=star))
