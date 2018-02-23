from Lib.Core import GlobalManager
import os


config = {
    'driver': 'File',
    'Redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    },
    'File': {
        'path': os.path.join(GlobalManager.get('root'), 'Storage/Caches'),
    },
}
