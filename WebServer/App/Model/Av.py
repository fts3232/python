from . import Model


class Av(Model):

    def getTag(self, tag):
        return self._db.select('select TAG_ID,TAG_NAME from TAG where TAG_ID IN({tag})'.format(tag=tag))

    def getAllTag(self):
        return self._db.select('select TAG_ID,TAG_NAME from TAG')

    def getDownloadLink(self, movie_id):
        return self._db.select('select LINK,PUBLISH_TIME from DOWNLOAD_LINK where MOVIE_ID = :MOVIE_ID', {'MOVIE_ID': movie_id})

    def getMovie(self, options):
        where = []
        whereData = {}
        if('identifiers' in options):
            where.append("IDENTIFIER IN({})".format(','.join(options['identifiers'])))
            limit = ''
        else:
            limit = 'LIMIT {offset},{size}'.format(offset=options['offset'], size=options['size'])
        if(options['title'] is not None):
            where.append("IDENTIFIER LIKE :SEARCH OR TITLE LIKE :SEARCH")
            whereData = {'SEARCH': '%{search}%'.format(search=options['title'])}
        elif(options['star'] is not None):
            where.append("FIND_IN_SET(:STAR,STAR)")
            whereData = {'STAR': options['star']}
        elif(options['tag'] is not None):
            where.append("FIND_IN_SET(:TAG,TAG)")
            whereData = {'TAG': options['tag']}
        where = ' and '.join(where)
        if(where != ''):
            where = 'where ' + where
        sql = 'select MOVIE_ID,TITLE,IDENTIFIER,TAG,STAR,PUBLISH_TIME from MOVIE {where} ORDER BY UPDATED_TIME DESC,PUBLISH_TIME DESC,CREATED_TIME DESC {limit}'.format(limit=limit, where=where)
        return self._db.select(sql, whereData)

    def getSample(self, movie_id):
        return self._db.select('select URL from SAMPLE where MOVIE_ID = :MOVIE_ID', {'MOVIE_ID': movie_id})

    def getStar(self, star):
        return self._db.select('select STAR_ID,STAR_NAME from STAR where STAR_ID IN({star})'.format(star=star))
