import unittest
from FirebaseAdmin import FirebaseAdmin, House, auth

class TestFirebaseAdmin(unittest.TestCase):

    def setUp(self):
        self._admin = FirebaseAdmin()

        self._house = {
            "address": "34 Brightly Dr",
            "rent": 2500,
            "size": 5555,
            "bedNumber": 5,
            "bathNumber": 4,
            "amenities": {
                "Pets": False,
                "Smoking": False,
                "Public Transit": False,
                "Laundry": False,
                "Snow Removal": False,
                "Air Conditioning": False
            },
            "utilities": [
                {
                    "name": "Hydro",
                    "amount": 40.0,
                    "frequency": "weekly"
                }
            ],
            "landlordEmail": "sneyd.ryan.ryan1@gmail.com",
            "description": "This house offers no ammenities",
            "isPosted": False
        }
        self._landlord = {
            "firstName": "R",
            "lastName": "S",
            "email": "sneyd.ryan.ryan1@gmail.com",
            "password": "aaaaaa",
            "password2": "aaaaaa"
        }
        self._tenant = {
            "firstName": "R",
            "lastName": "S",
            "tenantEmail": "a@s.com",
            "landlordEmail": "sneyd.ryan.ryan1@gmail.com",
            "password": "aaaaaa",
            "password2": "aaaaaa"
        }

        self._profile = {    
            "firstName": "Rodrigo",
            "lastName": "Hurtado Molero",
            "bio": "dsafdasfafgdasfads",
            "email": "hurtadro@sheridancollege.ca",
            "houseAddress": "34 Brightly Dr"
        }


    def test_add_house_with_no_house_array_in_landlord(self):
        admin = FirebaseAdmin()
        landlord = self._landlord
        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)
        admin.add_house(self._house)

        landlordSnapshot = db.collection("Landlord").document(landlord["email"]).get()
        
        expected = landlordSnapshot.get("houses")
        
        self.assertTrue(len(expected) == 1, "Error in adding landlord reference")
      
        db.collection("House").document(self._house["address"]).delete()
        db.collection("Landlord").document(landlord["email"]).delete()


    def test_add_house_with_pre_existing_house_array(self):
        admin = FirebaseAdmin()
        house = self._house
        landlord = self._landlord
        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)

        admin.add_house(house)
        house["address"] = "57 Earlscourt Cres"
        admin.add_house(house)
        
        
        landlordSnapshot = db.collection("Landlord").document(landlord["email"]).get()
        expected = landlordSnapshot.get("houses")
        

        self.assertTrue(len(expected) == 2, "Error in adding landlord reference")

        db.collection("House").document(house["address"]).delete()
        db.collection("House").document("34 Brightly Dr").delete()
        db.collection("Landlord").document(landlord["email"]).delete()
        


    def test_add_house_obscure_address(self):
        admin = FirebaseAdmin()
        house = self._house
        house["address"] = "Pikwitonei Lake Rd"
        landlord = self._landlord
        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)

        admin.add_house(house)

        houseSnapshot = db.collection("House").document("Pikwitonei Lake Rd").get()
        expected = houseSnapshot.get("url")

        self.assertEqual(expected, "", "Error in getting obscure location")
        
        db.collection("House").document(self._house["address"]).delete()
        db.collection("Landlord").document(landlord["email"]).delete()

    def test_add_house_returns_successful_response_with_empty_house_array(self):
        admin = FirebaseAdmin()
        house = self._house
        landlord = self._landlord

        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)

        result = admin.add_house(house)

        self.assertEqual(result["Result"], "House added successfully", "Error in adding landlord reference")


        db.collection("House").document(house["address"]).delete()
        db.collection("Landlord").document(landlord["email"]).delete()
  
    def test_add_house_returns_successful_response_with_multiple_houses(self):
        admin = FirebaseAdmin()
        house = self._house
        landlord = self._landlord
        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)

        admin.add_house(house)
        house["address"] = "57 Earlscourt Cres"
        result = admin.add_house(house)

        

        self.assertEqual(result["Result"], "House added successfully", "Error in adding landlord reference")

        db.collection("House").document(house["address"]).delete()
        db.collection("House").document("34 Brightly Dr").delete()
        db.collection("Landlord").document(landlord["email"]).delete()
        

    def test_add_house_error_on_duplicate_entry(self):
        admin = FirebaseAdmin()
        house = self._house
        landlord = self._landlord

        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)
    
        
        admin.add_house(house)
        result = admin.add_house(house)
        
        self.assertEqual("Error: House already exists", result["Result"], "Error duplicate entry")


        db.collection("House").document(house["address"]).delete()
        db.collection("Landlord").document(landlord["email"]).delete()


    def test_get_landlord_houses(self):
        admin = FirebaseAdmin()
        house = self._house
        landlord = self._landlord

        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)
        result = admin.add_house(house)
     
        result = admin.get_landlord_houses(landlord["email"])

        house["profiles"] = []
        house["tenants"] = []
        house["url"] = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=43.85998%2C+-79.04542699999999&key=AIzaSyCmiAvoaqyTdJZFjWzvIGDXkDmwr4Xwrn4'
      
        self.assertTrue(result[0] == house, "Error on retiving the houses")
        

        db.collection("House").document(house["address"]).delete()
        db.collection("Landlord").document(landlord["email"]).delete()

    def test_get_landlord_houses_invalid_landlord(self):
        admin = FirebaseAdmin()
        result = admin.get_landlord_houses("adsfdasklfasd")
        self.assertEqual(result["Result"], "Error: Landlord does not exist")
        

    def test_get_landlord_houses_no_houses(self):
        admin = FirebaseAdmin()
        landlord = self._landlord

        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)
  
        result = admin.get_landlord_houses(landlord["email"])
        self.assertEqual(result["Result"], "No houses found", "error when no houses are in document")

        db.collection("Landlord").document(landlord["email"]).delete()

    def test_write_temp_landlord(self):
        admin = FirebaseAdmin()
        landlord = self._landlord

        db = admin.get_db_instance()

        admin.write_temp_landlord(landlord, "1234")
        tempLandlordRef = db.collection("TempLandlord").document(landlord["email"])
        self.assertEqual(tempLandlordRef.get().get("firstName"), landlord["firstName"], "error when adding temp landlord")

        tempLandlordRef.delete()

    def test_user_added_to_auth_verify_temp_landlord(self):
        admin = FirebaseAdmin()
        landlord = self._landlord

        db = admin.get_db_instance()

        admin.write_temp_landlord(landlord, "1234")
        tempLandlordRef = db.collection("TempLandlord").document(landlord["email"]).get()

        admin.verify_temp_landlord(tempLandlordRef.get("email"), "1234")
        user = auth.get_user_by_email(landlord["email"])

        self.assertEqual(user.email, landlord["email"], "error with firebase authentication")

        auth.delete_user(user.uid)
        db.collection("Landlord").document(landlord["email"]).delete()

    def test_verify_temp_landlord_invalid_token(self):
        admin = FirebaseAdmin()
        landlord = self._landlord

        db = admin.get_db_instance()

        admin.write_temp_landlord(landlord, "1234")
        tempLandlordRef = db.collection("TempLandlord").document(landlord["email"]).get()

        result = admin.verify_temp_landlord(tempLandlordRef.get("email"), "45678")
       
        self.assertEqual(result["Result"], "Error: Invalid token", "error with token validation")

        db.collection("Landlord").document(landlord["email"]).delete()


    def test_valid_user_added_to_firestore_verify_temp_landlord(self):
        admin = FirebaseAdmin()
        landlord = self._landlord

        db = admin.get_db_instance()

        admin.write_temp_landlord(landlord, "1234")
        tempLandlordSnapshot = db.collection("TempLandlord").document(landlord["email"]).get()

        admin.verify_temp_landlord(tempLandlordSnapshot.get("email"), "1234")
        
        landlordSnapshot = db.collection("Landlord").document(landlord["email"]).get()

        self.assertEqual(landlordSnapshot.get("firstName"), landlord["firstName"], "error with firebase adding landlord")

        user = auth.get_user_by_email(landlord["email"])
        auth.delete_user(user.uid)
        db.collection("Landlord").document(landlord["email"]).delete()


    def test_valid_user_get_landlord(self):
        admin = FirebaseAdmin()
        landlord = self._landlord
        
        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)

        result = admin.get_landlord_by_email(landlord["email"])
        landlordSnapshot = db.collection("Landlord").document(landlord["email"]).get()

        self.assertEqual(landlordSnapshot.get("firstName"), landlord["firstName"], "error retriving landlord from firestore")
        db.collection("Landlord").document(landlord["email"]).delete()

    def test_email_not_found_get_landlord(self): 
        admin = FirebaseAdmin()
        landlord = self._landlord
        
        result = admin.get_landlord_by_email(landlord["email"])

        self.assertEqual("Error: Landlord not found", result["Result"], "error retriving landlord from firestore")

    def test_valid_user_get_tenant(self):
        admin = FirebaseAdmin()
        tenant = self._tenant
        
        db = admin.get_db_instance()
        db.collection("Tenant").document(tenant["tenantEmail"]).set(tenant)

        admin.get_tenant_by_email(tenant["tenantEmail"])
        tenantSnapshot = db.collection("Tenant").document(tenant["tenantEmail"]).get()

        self.assertEqual(tenantSnapshot.get("firstName"), tenant["firstName"], "error retriving tenant from firestore")
        db.collection("Tenant").document(tenant["tenantEmail"]).delete()

    def test_email_not_found_get_tenant(self): 
        admin = FirebaseAdmin()
        tenant = self._tenant
        
        result = admin.get_tenant_by_email(tenant["tenantEmail"])

        self.assertEqual("Error: Tenant not found", result["Result"], "error retriving tenant from firestore")


    def test_add_profile(self):
        admin = FirebaseAdmin()
        profile = self._profile
        admin.write_profile(profile)

        db = admin.get_db_instance()
        readProfile = db.collection("Profile").document(profile["email"]).get()

        self.assertEqual(readProfile.to_dict(), profile, "Error: write profile did not write profile correctly to firestore")
     
        db.collection("Profile").document(profile["email"]).delete()
      

    def test_duplicate_profile(self):
        admin = FirebaseAdmin()
        profile1 = self._profile
        admin.write_profile(profile1)

        profile2 = self._profile
        profile2["bio"] = "dxzafdasfadsfsadc"
        result = admin.write_profile(profile2)

        self.assertEqual(result["Result"], "Error: Profile already exists", "error with duplicate profile")
        db = admin.get_db_instance()
        db.collection("Profile").document(profile1["email"]).delete()
        db.collection("Profile").document(profile2["email"]).delete()

    
    def test_add_listings_post_listings(self):
        admin = FirebaseAdmin()
        house = self._house
        
        landlord = self._landlord
        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)
    
        admin.add_house(house)
        house["isPosted"] = True
        admin.post_listing(house)

        houseSnapshot = db.collection("House").document(house["address"]).get()
        self.assertTrue(houseSnapshot.get("isPosted"), "error posting to listings")

        db.collection("House").document(house["address"]).delete()
        db.collection("Landlord").document(landlord["email"]).delete()

    def test_add_profile_to_house(self):
        admin = FirebaseAdmin()
        house = self._house
        profile = self._profile
        
        landlord = self._landlord
        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)

       
        admin.add_house(house)
        admin.addProfileToHouse(profile)


        houseSnapshot = db.collection("House").document(house["address"]).get()
        self.assertTrue(len(houseSnapshot.get("profiles")) == 1, "error adding profile to house")

        db.collection("House").document(house["address"]).delete()
        db.collection("Landlord").document(landlord["email"]).delete()

    def test_convert_profile_to_tenant(self):
        admin = FirebaseAdmin()
        house = self._house
        profile = self._profile
        landlord = self._landlord

        db = admin.get_db_instance()
        db.collection("Landlord").document(landlord["email"]).set(landlord)

        admin.write_profile(profile)
        admin.add_house(house)
        admin.addProfileToHouse(profile)
        admin.convertProfileToTenant(profile)

        houseSnapshot = db.collection("House").document(house["address"]).get()
      
        self.assertTrue(len(houseSnapshot.get("tenants")) == 1, "error converting profile to tenant")

        db.collection("House").document(house["address"]).delete()
        db.collection("Landlord").document(landlord["email"]).delete()
        db.collection("Tenant").document(self._profile["tenantEmail"]).delete()
   

def test_get_tenant_houses(self):
    admin = FirebaseAdmin()
    house = self._house
    profile = self._profile
    landlord = self._landlord

    db = admin.get_db_instance()
    db.collection("Landlord").document(landlord["email"]).set(landlord)

    admin.write_profile(profile)
    admin.add_house(house)
    admin.addProfileToHouse(profile)
    admin.convertProfileToTenant(profile)
    
    result = admin.get_tenant_house(profile["tenantEmail"])

    house["profiles"] = []
    house["tenants"] = []
    house["url"] = 'https://maps.googleapis.com/maps/api/streetview?size=600x300&location=43.85998%2C+-79.04542699999999&key=AIzaSyCmiAvoaqyTdJZFjWzvIGDXkDmwr4Xwrn4'
    
    self.assertTrue(result == house, "Error on retiving the houses")
    

    db.collection("House").document(house["address"]).delete()
    db.collection("Tenant").document(profile["tenantEmail"]).delete()
