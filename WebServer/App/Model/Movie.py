class Movie():
    __db = None

    def __init__(self, db):
        self.__db = db

    def get(self, options):
        where = []
        whereData = {}
        if('identifiers' in options):
            where.append("IDENTIFIER IN({})".format(','.join(options['identifiers'])))
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
        sql = 'select MOVIE_ID,TITLE,IDENTIFIER,TAG,STAR,PUBLISH_TIME from MOVIE {where} ORDER BY UPDATED_TIME DESC,PUBLISH_TIME DESC,CREATED_TIME DESC LIMIT {offset},{size}'.format(offset=options['offset'], size=options['size'], where=where)
        return self.__db.select(sql, whereData)
