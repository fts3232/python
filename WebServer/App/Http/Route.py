class Route():
    __router = None

    def __init__(self, router):
        self.__router = router
        self.build()

    def build(self):
        self.__router.get('socket', 'Http.Controllers.Socket@Socket')
        self.__router.get('getData/?(\w*)$', 'Http.Controllers.GetData@GetData')
        self.__router.get('api/?(\w*)$', 'Http.Controllers.Api@Api')
        self.__router.get('cashBook/?(\w*)$', 'Http.Controllers.CashBook@CashBook')
