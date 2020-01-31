from Component import Component

class Amenity(Component):

    _name = ""
    _checked = False

    def __init__(self, name, checked):
        self._name = name
        self._checked = checked

    def get_dictionary(self):
        d = {
            "name": self._name,
            "checked": self._checked
        }
        return d

    def add_leaf(self, leaf):
        pass