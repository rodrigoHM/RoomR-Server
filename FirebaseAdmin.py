import firebase_admin
from firebase_admin import credentials, auth, messaging
from firebase_admin import firestore, storage
from House import House, Utility, Amenity, Profile, Tenant
from Landlord import Landlord
from Location import Location
from RepairRating import RepairRating
from Prediction import Prediction
import google
import datetime
from PIL import Image



class FirebaseAdmin():
    cred = credentials.Certificate('./ServiceAccount.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket' : 'roomr-222721.appspot.com'
    })
    def __init__(self):
        self._cred = credentials.Certificate('./ServiceAccount.json')
        self._db = firestore.client()
        self._transaction = self._db.transaction()
        self._houseRef = self._db.collection("House").document("11 Bronte Rd")

    def get_db_instance(self):
        return self._db

    def add_house(self, houseRequest):
        if (self._db.collection("House").document(houseRequest["address"]).get().exists):
            return {"Result": "Error: House already exists"}

        houseRef = self._db.collection("House").document(houseRequest["address"])
        landlordRef = self._db.collection("Landlord").document(houseRequest["landlordEmail"])
      
        location = Location()
        locationData = location.get_location_from_address(houseRequest["address"])
    
        house = House(houseRequest["address"], 
                    houseRequest["rent"], 
                    houseRequest["size"], 
                    houseRequest["bedNumber"], 
                    houseRequest["bathNumber"], 
                    houseRequest["landlordEmail"], 
                    locationData["url"], 
                    houseRequest["description"], 
                    False, 
                    houseRequest["amenities"], 
                    houseRequest["utilities"])

        houseRef.set(house.get_dictionary())
        houseRef.update({
            "province": locationData["province"],
            "city": locationData["city"]
        })

        houses = []
        landlordSnapshot = landlordRef.get()
        try:
            houseReferences = landlordSnapshot.get("houses")
          
            for reference in houseReferences:
                houses.append(reference)
         
            houses.append(houseRef.get().reference)
            landlordRef.update({"houses": houses})
        except KeyError:
            houses.append(houseRef.get().reference)
            landlordRef.update({"houses": houses})

        return {"Result": "House added successfully"}
    

      
            

        


    def get_landlord_houses(self, email):
        landlordHouses = []
    
        landlordSnapshot = self._db.collection("Landlord").document(email).get()
        if not landlordSnapshot.exists:
            return {"Result": "Error: Landlord does not exist"}

        try:
            for reference in landlordSnapshot.get("houses"):
                houseReference = self._db.document(reference.path).get()
                
                house = House(houseReference.get("address"), 
                                houseReference.get("rent"),
                                houseReference.get("size"),
                                houseReference.get("bedNumber"),
                                houseReference.get("bathNumber"),
                                houseReference.get("landlordEmail"),
                                houseReference.get("url"),
                                houseReference.get("description"),
                                houseReference.get("isPosted"),
                                houseReference.get("amenities"),
                                houseReference.get("utilities"))
                try: 
                    for profileReference in houseReference.get("profiles"):
                        profile = self._db.document(profileReference.path).get()
                        p = Profile(profile.get("firstName"),
                                    profile.get("lastName"),
                                    profile.get("email"),
                                    profile.get("bio"))
                    
                        house.add_leaf(p)
                except KeyError:
                    pass
                try:
                    for tenantReference in houseReference.get("tenants"):
                       
                        tenant = self._db.document(tenantReference.path).get()
                        t = Tenant(tenant.get("firstName"),
                                    tenant.get("lastName"),
                                    tenant.get("password"),
                                    tenant.get("password2"),
                                    tenant.get("tenantEmail"),
                                    tenant.get("landlordEmail"),
                                    tenant.get("tenantRating")) 
                        house.add_leaf(t)
                except KeyError:
                    pass

                landlordHouses.append(house.get_dictionary())
        except KeyError:
            return {"Result": "No houses found"}
        
        return landlordHouses

    def write_temp_landlord(self, landlord, uuid):
        tempLandlordRef = self._db.collection("TempLandlord").document(landlord["email"])
        tempLandlordRef.set(landlord)
        tempLandlordRef.update({"uuid": str(uuid)})
     

    def addUserToAuthentication(self, email, password):
        auth.create_user(email = email, password = password)

    def verify_temp_landlord(self, email, token):
        documents = self._db.collection("TempLandlord").get()
        for document in documents:
            if str(document.get("uuid")) == token:
                auth.create_user(email = email, password = document.get("password"))
                landlord = Landlord(document.get("firstName"), document.get("lastName"), document.get("email"), document.get("password"), document.get("password2"))
                self._db.collection("Landlord").document(email).set(landlord.get_dictionary())
                self._db.collection("TempLandlord").document(email).delete()
                return {"Result": "User successfully verified"}
            else:
                return {"Result": "Error: Invalid token"}

    def get_landlord_by_email(self, email):
        for document in self._db.collection("Landlord").get():
        
            if str(document.get("email")) == email:
                landlord = Landlord(document.get("firstName"), document.get("lastName"), document.get("email"), document.get("password"), document.get("password2")) 
                return landlord.get_dictionary()
        
        return {"Result": "Error: Landlord not found"}
            

    def get_tenant_by_email(self, email):
        for document in self._db.collection("Tenant").get():
           
            if str(document.get("tenantEmail")) == email:
                tenant = Tenant(document.get("firstName"), document.get("lastName"), document.get("password"), document.get("password2"), document.get("tenantEmail"), document.get("landlordEmail"), document.get("tenantRating"))
                return tenant.get_dictionary()
         
        return {"Result": "Error: Tenant not found"}
                

 
    def write_profile(self, profile):
        profileSnapshot = self._db.collection("Profile").document(profile["email"]).get()
        if profileSnapshot.exists:
            return {"Result": "Error: Profile already exists"}
        else:
            self._db.collection("Profile").document(profile["email"]).set(profile)
            return {"Result": "Profile successfully added"}

    def update_profile(self, profile):
        profileSnapshot = self._db.collection("Profile").document(profile["email"]).get()
        if profileSnapshot.exists:
            if profile["email"] == profileSnapshot.get("email"):
                self._db.collection("Profile").document(profile["email"]).update(profile)
                

    def post_listing(self, house):
        houseReference = self._db.collection("House").document(house["address"])
        houseReference.update({"isPosted": house["isPosted"]})
 

    def addPictureToStorage(self, image):
        bucket = storage.bucket()
        blob = bucket.blob("Repairs/Test.png")
        blob.upload_from_string(
            image,
            content_type='image/png'
        )
        blob.make_public()
        
        print(blob.public_url)

    def addProfileToHouse(self, profile):
        profileReferences = []
        houseSnapshot = self._db.collection("House").document(profile["houseAddress"]).get()
        try:
            for reference in houseSnapshot.get("profiles"):
                profileReferences.append(reference)
        except KeyError:
             self._db.collection("House").document(profile["houseAddress"]).update({"profiles": []})
        profileRef = self._db.collection("Profile").document(profile["email"])
        profileReferences.append(profileRef)
        self._db.collection("House").document(profile["houseAddress"]).update({"profiles": profileReferences})

    def search_houses(self, province, city, price, amenities):
        filteredHouses = []
        houseCollection = self._db.collection("House").get()
        for houseDocument in houseCollection:
            if houseDocument.get("isPosted") == True:
                if houseDocument.get("province") == province:
                    if houseDocument.get("city") == city:
                        if houseDocument.get("rent") <= price:
                            if houseDocument.get("amenities") == amenities:
                                house = House(houseDocument.get("address"), 
                                houseDocument.get("rent"),
                                houseDocument.get("size"),
                                houseDocument.get("bedNumber"),
                                houseDocument.get("bathNumber"),
                                houseDocument.get("landlordEmail"),
                                houseDocument.get("url"),
                                houseDocument.get("description"),
                                houseDocument.get("isPosted"),
                                houseDocument.get("amenities"),
                                houseDocument.get("utilities"))
                                try: 
                                    for profileReference in houseDocument.get("profiles"):
                                        profile = self._db.document(profileReference.path).get()
                                        p = Profile(profile.get("firstName"),
                                                    profile.get("lastName"),
                                                    profile.get("email"),
                                                    profile.get("bio"))
                                    
                                        house.add_leaf(p)
                                except KeyError:
                                    pass
                                try:
                                    for tenantReference in houseDocument.get("tenants"):
                                    
                                        tenant = self._db.document(tenantReference.path).get()
                                        t = Tenant(tenant.get("firstName"),
                                                    tenant.get("lastName"),
                                                    tenant.get("password"),
                                                    tenant.get("password2"),
                                                    tenant.get("tenantEmail"),
                                                    tenant.get("landlordEmail"),
                                                    tenant.get("tenantRating"))
                                        house.add_leaf(t)
                                except KeyError:
                                    pass

                                filteredHouses.append(house.get_dictionary())
        return filteredHouses


    def convertProfileToTenant(self, profile): 
        houseReference = self._db.collection("House").document(profile["houseAddress"]).get()
        address = profile["houseAddress"]
        del profile["houseAddress"]
    
        profileReferences = []
        tenantReferences = []
        for profileReference in houseReference.get("profiles"):
            
            if self._db.document(profileReference.path).get().to_dict() == profile:
               
                del profile["bio"]
                profile["tenantEmail"] = profile["email"]
                del profile["email"]
 
                self._db.collection("Tenant").document(profile["tenantEmail"]).set(profile)
                tenantReferences.append(self._db.collection("Tenant").document(profile["tenantEmail"]).get().reference)
            else:    
                profileReferences.append(profileReference)

        for houseDocument in self._db.collection("House").stream():
            houseProfileList = houseDocument.get("profiles")
            for profileReference in houseProfileList:
                profileSnapshot = self._db.document(profileReference.path).get()
                if profileSnapshot.get("email") == profile["tenantEmail"]:
                    houseProfileList.remove(profileReference)
            houseDocument.reference.update({"profiles": houseProfileList})

        self._db.collection("Tenant").document(profile["tenantEmail"]).update({"houseReference": self._db.collection("House").document(address)})
        self._db.collection("House").document(address).update({"profiles": profileReferences, "tenants": tenantReferences})

    def sign_up_tenant(self, tenant):
        tenantReferance = self._db.collection("Tenant").document(tenant["tenantEmail"]).get()
        if (tenantReferance.get("firstName") == tenant["firstName"] and tenantReferance.get("lastName") == tenant["lastName"]):
            self._db.collection("Tenant").document(tenant["tenantEmail"]).update(tenant)
            self.addUserToAuthentication(tenant["tenantEmail"], tenant["password"])

    def add_payment_landlord(self, paymentId):
        paymentRef = self._db.collection("Payment").document(paymentId).get()
        payment = paymentRef.to_dict()

        payments = []
        landlordRef = self._db.collection("Landlord").document(payment["landlordEmail"]).get()
        try:
            paymentNotifications = landlordRef.get("payments")
        
            print(paymentNotifications)
        except KeyError:
            self._db.collection("Landlord").document(payment["landlordEmail"]).update({"payments": [payment]})
            return
            
        for paymentNotification in paymentNotifications:
            payments.append(paymentNotification)
        payments.append(payment)
        self._db.collection("Landlord").document(payment["landlordEmail"]).update({"payments": payments})

    def add_pending_payment(self, payment, paymentId):
        self._db.collection("Payment").document(paymentId).set(payment)

    def get_landlord_payments(self, landlordEmail):
        landlordRef = self._db.collection("Landlord").document(landlordEmail).get()
        return landlordRef.get("payments")

    def get_tenant_house(self, tenantEmail):
        tenantSnapshot = self._db.collection("Tenant").document(tenantEmail).get()
        reference = tenantSnapshot.get("houseReference")
        print(reference)
        houseSnapshot = self._db.document(reference.path).get()
        house = House(houseSnapshot.get("address"), 
                        houseSnapshot.get("rent"),
                        houseSnapshot.get("size"),
                        houseSnapshot.get("bedNumber"),
                        houseSnapshot.get("bathNumber"),
                        houseSnapshot.get("landlordEmail"),
                        houseSnapshot.get("url"),
                        houseSnapshot.get("description"),
                        houseSnapshot.get("isPosted"),
                        houseSnapshot.get("amenities"),
                        houseSnapshot.get("utilities"))

        for profileReference in houseSnapshot.get("profiles"):
            profile = self._db.document(profileReference.path).get()
            p = Profile(profile.get("firstName"),
                        profile.get("lastName"),
                        profile.get("email"),
                        profile.get("bio"))
            house.add_leaf(p)
        try:
            for tenantReference in houseSnapshot.get("tenants"):
                tenant = self._db.document(tenantReference.path).get()
                t = Tenant(tenant.get("firstName"),
                            tenant.get("lastName"),
                            tenant.get("password"),
                            tenant.get("password2"),
                            tenant.get("tenantEmail"),
                            tenant.get("landlordEmail"),
                            tenant.get("tenantRating"))
                house.add_leaf(t)
        except KeyError:
            print("Error: Tenant key error")
        return house.get_dictionary()

    def get_tenants_from_houses(self, email):
        landlordSnapshot = self._db.collection("Landlord").document(email).get()
        houses = landlordSnapshot.get("houses")
        results = []
        for house in houses:
            result = {}
            houseSnapshot = self._db.document(house.path).get()
            if houseSnapshot:
                result["houseAddress"] = houseSnapshot.get("address")
            
                for tenantReference in houseSnapshot.get("tenants"):
                    tenantSnapshot = self._db.document(tenantReference.path).get()
                    result["tenantName"] = tenantSnapshot.get("firstName") + " " + tenantSnapshot.get("lastName")
                    results.append(result)
        return results


    def send_repair_notification(self, landLordEmail):
        # This registration token comes from the client FCM SDKs.
        landlordSnapshot = self._db.collection("Landlord").document(landLordEmail).get()
        registration_token = landlordSnapshot.get("token")
        print(registration_token)

        notification = messaging.Notification(title="RoomR", body="Reminder, New Repairs has been posted.")


        message = messaging.Message(
            notification=notification,
            token=registration_token
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        print(response)

    def send_payment_notification(self, tenantEmail):
        # This registration token comes from the client FCM SDKs.
        tenantSnapshot = self._db.collection("Tenant").document(tenantEmail).get()
        registration_token = tenantSnapshot.get("token")
        print(registration_token)
        #registration_token = 'dgbUdtkPs5w:APA91bGOZBTSbcsIyaAIhMTyJPOUC0VTH0FdSa5IowZnd408x0mNzwnpkj7rXu5SbVKgiQzqy9n-wXVqGRlQqx8lGfOtafHM6O0tKV2H6bwdDNFTjHdyD4n1quQEpwKH2_2wXZocy1ew'
       
        notification = messaging.Notification(title="RoomR", body="Reminder, Rent is coming up.")


        message = messaging.Message(
            notification=notification,
            token=registration_token
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        print(response)

    def is_uid_valid(self, token):
        try:
            auth.get_user(token)
            return True
        except auth.AuthError:
            return False

    def update_house(self, locationRequest):
        houseReference = self._db.collection("House").document(locationRequest["houseAddress"])
        locaction = Location()
        print(locaction.retry_location(locationRequest["houseAddress"]))
        houseReference.update({"url": locaction.retry_location(locationRequest["houseAddress"]), "province": locationRequest["province"], "city": locationRequest["city"]})

    def remove_house(self, house):
        houseReference = self._db.collection("House").document(house["address"])
        houseReference.delete()
        landlordSnapshot = self._db.collection("Landlord").document(house["landlordEmail"]).get()
        houses = landlordSnapshot.get("houses")
        for houseRef in houses:
           
            if houseRef.path == houseReference.path:
                houses.remove(houseRef)
        self._db.collection("Landlord").document(house["landlordEmail"]).update({"houses": houses})


    def update_repairs(self, houseAddress, date, repairs):
        self._db.collection('House').document(houseAddress).collection("Repairs").document(date).update(repairs)

    def update_repairs_landlord(self, houseAddress, date, dateUpdated):
        repairRating = 0.00
        #Getting Landlord Email.
        houseSnapshot = self._db.collection("House").document(houseAddress).get()
        landLordEmail = houseSnapshot.get("landlordEmail")
        
        #Check if rating exist if not make one, if it does pull it and get the rating.
        landlordDocument = self._db.collection("Landlord").document(landLordEmail).get()
        landlordDictionary = landlordDocument.to_dict()
        if("repairrating" in landlordDictionary):
            repairRating = float(landlordDictionary["repairrating"])
        else:
            repairRating = 5.00
            ratingRepair = {u"repairrating": str(repairRating)}
            self._db.collection("Landlord").document(landLordEmail).update(ratingRepair)

        #Object of RepairRating
        repairRatingObj = RepairRating(date, dateUpdated, landLordEmail)
        calculatedRating = repairRatingObj.calculateRating()
        
        #Get value from repairRatingCLass add it to the repairRating and update.
        #repairRating = RepairRating.getRating()
        repairRating = repairRating + calculatedRating
        if(repairRating >= 5.00):
            repairRating = 5.00
        if(repairRating <= 0.00):
            repairRating = 0.00
        repairRating = round(repairRating, 2)
        ratingRepair = {u"repairrating": float(repairRating)}
        self._db.collection("Landlord").document(landLordEmail).update(ratingRepair)
        #date has to be in month and year format.
        date = repairRatingObj.getDateUpdated()
        rating = {u"date": date, u"rating": float(repairRating)}
        self._db.collection("RepairRatings").document(landLordEmail).collection("Rating").document(date).set(rating)

    def getRepairRatingHistory(self, landlordEmail):
        ratingHistoryList = []
        try:
            docs = self._db.collection("RepairRatings").document(landlordEmail).collection("Rating")
            doctsToStream = docs.stream()
            for doc in doctsToStream:
                dictonaryOfRatingHistory = doc.to_dict()
                ratingHistoryList.append(dictonaryOfRatingHistory)
        except google.cloud.exceptions.NotFound:
            ratingHistoryList.append({'error':'Not such repair Rating for this Landlord.'})
            print(u'No Such Document')

        return ratingHistoryList

    def get_repairs_for_house(self, houseAddress):
        documents = self._db.collection("House").document(houseAddress).collection("Repairs")
        #To get photo we will just send back the link to the photo and from the app it will get the photos.
        repairList = []
        try:
            docs = documents.stream()
            for doc in docs:
                dictionayOfRepair = doc.to_dict()
                repairList.append(dictionayOfRepair)

        except google.cloud.exceptions.NotFound:
            repairList.append({'error':'Not such repairs for this house.'})
            print(u'No Such Document')

        return repairList

    def predict_image(self, imgUrl, language):
        prediction = Prediction(imgUrl,language)
        return prediction.getWordsRelatedToImage()
    


    def get_landlord_rating(self, houseAddress):
        houseSnapshot = self._db.collection("House").document(houseAddress).get()
        landLordEmail = houseSnapshot.get("landlordEmail")

        landlordDocument = self._db.collection("Landlord").document(landLordEmail).get()
        rating = landlordDocument.get("repairrating")
        return rating

    def add_repair(self, houseAddress, date, repairs):
        self._db.collection('House').document(houseAddress).collection("Repairs").document(date).set(repairs)