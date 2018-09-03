# import os
from . import Controller
from Model.CashBook import CashBook as CashBookModel


class CashBook(Controller):

    def get(self):
        try:
            page = int(self.getArgument('page', default=1))
            size = int(self.getArgument('size', default=10))
            cashBook = CashBookModel()
            ret = cashBook.get(page,size)
            total = cashBook.getCount()
        except BaseException as err:
            print(err)
            result = {'status':False}
        else:
            result = {'status':True,'ret':ret,'total':total}
        self.json(result)

    def add(self):
        try:
            data = {'DATE':self.getArgument('date'),'AMOUNT':self.getArgument('amount'),'TYPE':self.getArgument('type'),'DESCRIPTION':self.getArgument('description'),'TAGS':self.getArgument('tag')}
            cashBook = CashBookModel()
            ret = cashBook.add(data)
        except BaseException as err:
            print(err)
            result = {'status':False}
        else:
            result = {'status':True}
        self.json(result)