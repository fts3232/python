from abc import ABC, abstractmethod


class Factory(ABC):

    _config = {}

    def __init__(self, config):
        self._config = config

    @abstractmethod
    def write(self, exc_info):
        pass
