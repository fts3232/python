class Route():
    __router = None

    def __init__(self, router):
        self.__router = router
        self.build()

    def build(self):
        self.__router.get('socket', 'Http.Controllers.Socket@Socket')
        self.__router.get('getData/?(\w*)$', 'Http.Controllers.GetData@GetData')
