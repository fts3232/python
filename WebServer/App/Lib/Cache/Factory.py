from abc import ABC, abstractmethod


class Factory(ABC):

    _config = {}

    def __init__(self, config):
        self._config = config

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value, second):
        pass

    @abstractmethod
    def has(self, key):
        pass

    @abstractmethod
    def delete(self, key):
        pass
