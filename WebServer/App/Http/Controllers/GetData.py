# import os
from . import Controller
from Business.Av import Av
from Business.Comic import Comic


class GetData(Controller):

    def av(self):
        business = Av(self._app.make('Config').get('Av'))
        p = int(self.getArgument('p', default=1))
        size = int(self.getArgument('size', default=12))
        title = self.getArgument('title', default=None)
        star = self.getArgument('star', default=None)
        tag = self.getArgument('tag', default=None)
        canPlay = True if self.getArgument('canPlay', default=0) == '1' else False
        offset = (p - 1) * size
        options = {'size': size, 'title': title, 'star': star, 'tag': tag, 'offset': offset}
        if(canPlay is True):
            identifiers = business.scanLocalFolder()
            if(options['title'] is None and options['star'] is None and options['tag'] is None):
                identifiers = identifiers[offset:offset + size]
            options['identifiers'] = identifiers
        ret = business.getData(options)
        self.json(ret)

    def comic(self):
        ret = Comic().run()
        self.json(ret)

    def tag(self):
        ret = Av(self._app.make('Config').get('Av')).getTag()
        self.json(ret)
