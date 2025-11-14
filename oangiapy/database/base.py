from abc import ABC, abstractmethod

class BaseDB(ABC):
    @abstractmethod
    def create(self, collection, data):
        pass

    @abstractmethod
    def read(self, collection, query=None):
        pass

    @abstractmethod
    def update(self, collection, doc_id, data):
        pass

    @abstractmethod
    def delete(self, collection, doc_id):
        pass