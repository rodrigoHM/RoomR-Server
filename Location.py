import google_streetview.api
from googlegeocoder import GoogleGeocoder
import os

class Location():
    def __init__(self):
        self._api_key = "AIzaSyCmiAvoaqyTdJZFjWzvIGDXkDmwr4Xwrn4"


    def get_location_from_address(self, address):
        geocoder = GoogleGeocoder(self._api_key)
        locationData = {}
        try:
            search = geocoder.get(address)
        except ValueError:
            locationData["city"] = ""
            locationData["province"] = ""
            locationData["url"] = ""
            return locationData

        params = [{
            'size': '600x300', # max 640x640 pixels
            'location': str(search[0].geometry.location.lat) + ', ' + str(search[0].geometry.location.lng),
            'key': self._api_key
        }]

        results = google_streetview.api.results(params)
        addressComponents = search[0].address_components
       
        if len(addressComponents) == 7:

            for addressComponent in addressComponents:
                if addressComponent.types == ['locality', 'political']:
                    locationData["city"] = addressComponent.long_name
                if addressComponent.types == ['administrative_area_level_1', 'political']:
                    locationData["province"] = addressComponent.long_name
            locationData["url"] = results.links[0]
        else:

            locationData["city"] = ""
            locationData["province"] = ""
            locationData["url"] = ""



        return locationData


    def retry_location(self, address):
        geocoder = GoogleGeocoder(self._api_key)
        locationData = {}
        try:
            search = geocoder.get(address)
        except ValueError:
            return ""

        params = [{
            'size': '600x300', # max 640x640 pixels
            'location': str(search[0].geometry.location.lat) + ', ' + str(search[0].geometry.location.lng),
            'key': self._api_key
        }]

        results = google_streetview.api.results(params)
        return results.links[0]