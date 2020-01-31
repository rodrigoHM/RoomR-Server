from Component import Component

class Utility(Component):

    _name = ""
    _frequency = ""
    _amount = 0

    def __init__(self, name, frequency, amount):
        self._name = name
        self._frequency = frequency
        self._amount = amount

    def get_dictionary(self):
        d = {
            "name": self._name,
            "frequency": self._frequency,
            "amount": self._amount
        }
        return d
    
    def add_leaf(self, leaf):
        pass
    