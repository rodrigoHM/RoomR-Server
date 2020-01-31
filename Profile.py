from Component import Component

class Profile(Component):

    _firstName = ""
    _lastName = ""
    _email = ""
    _bio = ""

    def __init__(self, firstName, lastName, email, bio):
        self._firstName = firstName
        self._lastName = lastName
        self._email = email
        self._bio = bio

    def get_dictionary(self):
        d = {
            "firstName": self._firstName,
            "lastName": self._lastName,
            "email": self._email,
            "bio": self._bio
        }
        return d
    
    def add_leaf(self, leaf):
        pass
    