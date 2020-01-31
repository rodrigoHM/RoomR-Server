from Component import Component
from Utility import Utility
from Amenity import Amenity
from Profile import Profile
from Tenant import Tenant

class House(Component):
    _address = ""
    _rent = 0
    _size = 0
    _bedNumber = 0
    _bathNumber = 0
    _landlordEmail = ""
    _description = ""
    _url = ""
    _isPosted = False


    def __init__(self, address, rent, size, bedNumber, bathNumber, landlordEmail, url, description, isPosted, amenities, utilities):
        self._address = address
        self._rent = rent
        self._size = size
        self._bedNumber = bedNumber
        self._bathNumber = bathNumber
        self._landlordEmail = landlordEmail
        self._url = url
        self._description = description
        self._isPosted = isPosted
        self._amenities = amenities
        self._utilities = utilities
        self._profiles = []
        self._tenants = []
    
    def get_dictionary(self):
        d = {
            "address": self._address,
            "rent": self._rent,
            "size": self._size,
            "bedNumber": self._bedNumber,
            "bathNumber": self._bathNumber,
            "landlordEmail": self._landlordEmail,
            "url": self._url,
            "description": self._description,
            "isPosted": self._isPosted,
            "amenities": self._amenities,
            "utilities": self._utilities,
            "profiles": self._profiles,
            "tenants": self._tenants
        }
        return d

    def add_leaf(self, leaf):
        if isinstance(leaf, Utility):
            self._utilities.append(leaf.get_dictionary())
        if isinstance(leaf, Amenity):
            self._amenities.append(leaf.get_dictionary())
        if isinstance(leaf, Profile):
            self._profiles.append(leaf.get_dictionary())
        if isinstance(leaf, Tenant):
            self._tenants.append(leaf.get_dictionary())