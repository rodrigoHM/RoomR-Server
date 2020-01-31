import unittest
from Location import Location

class TestLocation(unittest.TestCase):

    def setUp(self):
        self.location = Location()


    def test_location_with_valid_address(self):
        expected = self.location.get_location_from_address("34 Brightly Dr")
        actual =  {'city': 'Ajax', 'province': 'Ontario', 'url': 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=43.85998%2C+-79.04542699999999&key=AIzaSyCmiAvoaqyTdJZFjWzvIGDXkDmwr4Xwrn4'}

        self.assertEqual(expected, actual, "error with getting location data")

    def test_location_with_obscure_address(self):
        #Address is street somewhere in the middle of Manitoba
        expected = self.location.get_location_from_address("Pikwitonei Lake Rd")
        actual =  {'city': '', 'province': '', 'url': ''}

        self.assertEqual(expected, actual, "error with getting obscure location data")

    def test_location_with_jibberish(self):
        expected = self.location.get_location_from_address("dsabfjkdasnjfnlkdsanfa")
        actual =  {'city': '', 'province': '', 'url': ''}

        self.assertEqual(expected, actual, "error with jibberish data")