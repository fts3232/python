from . import Model


class Tag(Model):

    def get(self, tag):
        return self._db.select('select TAG_ID,TAG_NAME from TAG where TAG_ID IN({tag})'.format(tag=tag))

    def getAll(self):
        return self._db.select('select TAG_ID,TAG_NAME from TAG')
