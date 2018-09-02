# import os
from . import Controller
from Model.CashBook import CashBook


class Api(Controller):

    def createDB(self):
        try:
            cashBook = CashBook()
            ret = cashBook.createDB()
        except:
            result = {'status':False}
        else:
            result = {'status':True}
        self.json(result)