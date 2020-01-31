from Component import Component

class Tenant(Component):

    _firstName = ""
    _lastName = ""
    _password = ""
    _password2 = ""
    _tenantEmail = ""
    _landlordEmail = ""
    _tenantRating = ""

    def __init__(self, firstName, lastName, password, password2, tenantEmail, landlordEmail, tenantRating):
        self._firstName = firstName
        self._lastName = lastName
        self._password = password
        self._password2 = password2
        self._tenantEmail = tenantEmail
        self._landlordEmail = landlordEmail
        self._tenantRating = tenantRating

    def get_dictionary(self):
        d = {
            "firstName": self._firstName,
            "lastName": self._lastName,
            "password": self._password,
            "password2": self._password2,
            "tenantEmail": self._tenantEmail,
            "landlordEmail": self._landlordEmail,
            "tenantRating": self._tenantRating
        }
        return d
    
    def add_leaf(self, leaf):
        pass
    