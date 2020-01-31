from abc import ABC, abstractmethod

class Component(ABC):
    
    @abstractmethod
    def get_dictionary(self):
        pass

    @abstractmethod
    def add_leaf(self, leaf):
        pass