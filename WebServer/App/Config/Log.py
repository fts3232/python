from Lib.Core import GlobalManager
import os


config = {
    'driver': 'File',
    'File': {
        'path': os.path.join(GlobalManager.get('root'), 'Storage/Logs'),
    },
    'MongoDB': {
        'host': 'localhost',
        'port': 27017,
        'db': 'test'
    }
}
