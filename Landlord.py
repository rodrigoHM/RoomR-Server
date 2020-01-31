
class Landlord:

    def __init__(self, firstName, lastName, email, password, password2):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.password2 = password2
        self.houses = []

    def get_dictionary(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "password": self.password,
            "password2": self.password2
        }


