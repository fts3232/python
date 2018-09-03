from . import Model


class CashBook(Model):

    def createDB(self):
        sql = "CREATE TABLE CASH_BOOK(\
               `ROW_ID` INT NOT NULL AUTO_INCREMENT,\
               `TYPE` VARCHAR(30) NOT NULL,\
               `AMOUNT`  int(11) NULL ,\
               `TAGS`  varchar(255) NULL ,\
               `DESCRIPTION`  text NULL ,\
               `CREATED_AT` DATETIME DEFAULT CURRENT_TIMESTAMP,\
               PRIMARY KEY (`ROW_ID`)\
               )\
               ENGINE=InnoDB\
               DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;"
        ret = self._db.query(sql)
        return ret

    def get(self,page,size):
        offset = (page - 1) * size
        limit = ' LIMIT {offset},{size}'.format(offset=offset, size=size)
        sql = "SELECT ROW_ID,TYPE,AMOUNT,TAGS,DESCRIPTION,CREATED_AT FROM CASH_BOOK ORDER BY CREATED_AT DESC {limit} ".format(limit=limit)
        ret = self._db.select(sql)
        return ret

    def getCount(self):
        sql = "SELECT COUNT(*) FROM CASH_BOOK"
        ret = self._db.count(sql)
        return ret

    def add(self, params):
        self._db.begin()
        sql = "INSERT INTO CASH_BOOK (\
               	AMOUNT,\
               	TYPE,\
               	TAGS,\
               	DESCRIPTION,\
		DATE,\
               	CREATED_AT\
               )\
               VALUES\
               	(\
               		:AMOUNT,\
               		:TYPE,\
               		:TAGS,\
               		:DESCRIPTION,\
               		:DATE,\
			        NOW()\
               	)"
        ret = self._db.insert(sql,params)
        if(ret):
            self._db.commit()
        else:
            self._db.rollback()
        return ret;