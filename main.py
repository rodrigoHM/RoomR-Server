from flask import Flask, jsonify, request, redirect, send_from_directory
from Location import Location
from ast import literal_eval
from PIL import Image
from FirebaseAdmin import FirebaseAdmin
from firebase_admin import firestore, storage
from EmailServer import Email
from paypalrestsdk import Payment, Order
from Payment import PaymentOperations
import paypalrestsdk
from datetime import date, datetime
import json, uuid
from googleplaces import GooglePlaces, types, lang
from geopy.geocoders import Nominatim
app = Flask(__name__)

db = FirebaseAdmin()



@app.route("/AddHouse/<token>", methods=["POST", "GET"])
def add_house(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        res = db.add_house(req)
       
        return jsonify(res)
    return ""

@app.route("/GetHouse/<token>", methods=["POST"])
def get_house(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        
        json = db.get_landlord_houses(req["email"])
        return jsonify(json)
    return ""

@app.route("/SignUpTempLandlord/", methods=["POST"])
def sign_up_temp_landlord():
    global db
    
    token = uuid.uuid4()
    req = request.get_json()
    db.write_temp_landlord(req, token)
    email = Email(req["email"], req["firstName"], "https://roomr-222721.appspot.com/", token)
    email.sendEmail()
    return ""

@app.route("/AddLandlord/<token>/<email>")
def add_landlord(token, email):
    global db
    db.verify_temp_landlord(email, token)
    return "<h1>Landlord Added Successfully</h1>"

@app.route("/GetLandlord/<token>", methods=["POST"])
def get_landlord(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        json = db.get_landlord_by_email(req["userName"])
        
        return jsonify(json)
    return ""


@app.route("/GetTenant/<token>", methods=["POST"])
def get_tenant(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        json = db.get_tenant_by_email(req["userName"])
        return jsonify(json)
    return ""

@app.route("/AddProfile/<token>", methods=["POST"])
def add_profile(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        print(req)
        response = db.write_profile(req)
        print(response)
        return jsonify(response)
    return ""

@app.route("/PostListing/<token>", methods=["POST"])
def post_listing(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        print(req)   
        db.post_listing(req)
    return ""

@app.route("/UpdateProfile/<token>", methods=["POST"])
def update_profile(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        print(req)   
        db.update_profile(req)
    return ""


@app.route("/SearchListings/<token>", methods=["POST"])
def search_listing(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        houses = db.search_houses(req["province"], req["city"], req["price"], req["amenities"],)
        return jsonify(houses)
    return ""


@app.route("/ContactLandlord/<token>", methods=["POST"])
def contact_landlord(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        print(req)   
        db.addProfileToHouse(req)
    return ""

@app.route("/ContactProfile/<token>", methods=["POST"])
def contact_profile(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        email = Email(req["email"], req["firstName"], "10.16.25.74:8080", 0)
        email.sendContactProfileEmail()
    return ""
    
@app.route("/ConvertProfileToTenant/<token>", methods=["POST"])
def convert_profile_to_tenant(token):
    global db 
    if db.is_uid_valid(token):
        req = request.get_json()
        db.convertProfileToTenant(req)
    return ""

@app.route("/SignUpTenant/<token>", methods=["POST"])
def sign_up_tenant(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        print(req)
        db.sign_up_tenant(req)
    return ""

@app.route("/execute")
def execute():
  
    print("*************************TEST******************")
    executePayment = paypalrestsdk.Payment.find(request.args.get('paymentId'))
    try:
        if executePayment.execute({"payer_id": request.args.get('PayerID')}):
            print("Payment execute successfully")
            global db
            db.add_payment_landlord(request.args.get('paymentId'))
            return redirect("https://roomr-222721.appspot.com/PayComplete", code=200)
        else:
            print(executePayment.error) # Error Hash
            return "Failed"
    except:
        print(executePayment.error) # Error Hash
        return "Failed"

@app.route("/MakePayment/<token>", methods=["POST"])
def make_payment(token):
    global db
    if db.is_uid_valid(token):
        payment = PaymentOperations()
        req = request.get_json()
        
        
        return_tuple = payment.make_payment(req["amount"], "sb-ngv5p430179@business.example.com")
        today = date.today()
        pendingPayment = {
            "dueDate": req["dueDate"],
            "houseAddress": req["houseAddress"],
            "landlordEmail": req["landlordEmail"],
            "tenantName": req["tenantName"],
            "datePaid": str(today)
        }
        db.add_pending_payment(pendingPayment, return_tuple[1])
        
        response = {"response_url": return_tuple[0]}
        return jsonify(response)
    return ""

@app.route('/.well-known/<path:path>')
def send_json(path):
    return send_from_directory('.well-known', path)

@app.route("/GetLandlordPayments/<token>", methods=["POST"])
def get_landlord_payments(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        print(req)
        payments = db.get_landlord_payments(req["email"])
        return jsonify(payments)
    return ""

@app.route("/GetTenantHouse/<token>", methods=["POST"])
def get_tenant_house(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        print(req)
        house = db.get_tenant_house(req["tenantEmail"])
        return jsonify(house)
    return ""

@app.route("/SendPaymentNotification/<token>", methods=["POST"])
def test_notification(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        print(req)
        db.send_payment_notification(req["tenantEmail"])
    return ""


@app.route("/AddLocationToHouse/<token>", methods=["POST"])
def add_location_to_house(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        print(req)
        db.update_house(req)
    return ""

@app.route("/RemoveHouse/<token>", methods=["POST"])
def remove_house(token):
    global db
    if db.is_uid_valid(token):
        req = request.get_json()
        print(req)
        db.remove_house(req)
    return ""


@app.route("/UpdateRepairs", methods=["POST"])
def updateRepairs():
    global db
    data = request.get_json(cache=True)
    status = data["status"]
    description = data["description"]
    date = data["date"]
    houseAddress = data["houseAddress"]
    repairs = {u"Description":description, u"Status":status}
    db.update_repairs(houseAddress, date, repairs)
    return "WORKS"

@app.route("/UpdateRepairsLandlord", methods=["POST"])
def updateRepairsLandLord():
    global db
    data = request.get_json(cache=True)
    dateUpdated = data["dateUpdated"]
    status = data["status"]
    date = data["date"]
    houseAddress = data["houseAddress"]
    

    #Updates Repair
    repairs = {u"Status":status, u"DateUpdated":dateUpdated}
    db.update_repairs(houseAddress, date, repairs)
    db.update_repairs_landlord(houseAddress, date, dateUpdated)
    return "WORKS"

@app.route("/GetRepairRatingHistory", methods=["POST"])
def getRepiarRatingHistoryLandlord():
    global db
    data = request.get_json(cache=True)
    landLordEmail = data["landlordEmail"]
    ratingHistoryList = db.getRepairRatingHistory(landLordEmail)
    jsonData=json.dumps(ratingHistoryList)
    return jsonData

@app.route("/GetRepairs", methods=["POST"])
def getRepairsForHouse():
    global db
    data = request.get_json(cache=True)
    houseAddress = data["houseAddress"] 
    repairList = db.get_repairs_for_house(houseAddress)
    jsonData=json.dumps(repairList)
    return jsonData

@app.route("/AddPhoto", methods=["POST"])
def predictImageProblem():
    #Here will be the pre-train model to have a prediction of what the image is.
    #data = request.get_json(cache=True)
    global db
    if 'Photo' in request.files:
        photo = request.files['Photo']
    else:
        print("not photo")
    language = literal_eval(request.form["Language"])
    language = language["Language"]
    
    
    photo = photo.read()

    #change upload_from_filename to upload_from_string
    bucket = storage.bucket()
    #Image Name
    now = datetime.now()

    #Test.png is the name of the img.
    blobForBucket = bucket.blob("Repairs/" + str(now))
    blobForBucket.upload_from_string(
        photo,
        content_type='image/png'
    )
    blobForBucket.make_public()
    imgUrl = blobForBucket.public_url
    
    jsonResponse = db.predict_image(imgUrl, language)

    return jsonResponse

@app.route("/GetLandlordWithHouseAddress", methods=["POST"])
def getLandlordRatingByHouseAddress():
    global db
    data = request.get_json(cache=True)
    houseAddress = data["houseAddress"]

    rating = db.get_landlord_rating(houseAddress)

    json = {"repairrating": rating}
    return jsonify(json)

@app.route("/AddRepair", methods=["POST"])
def firebaseRepairInformation():
    global db 
    data = request.get_json(cache=True
    repairName = data["name"]
    status = data["status"]
    description = data["description"]
    photoURL = data["photoRef"]
    date = data["date"]
    dateUpdated = data["dateUpdated"]
    houseAddress = data["houseAddress"]
    landLordEmail = data["landlordEmail"]
    

    db.send_repair_notification(landLordEmail)
    
    repairs = {u"Name" : repairName, u"Description":description, u"Status":status, u"Date":date, u"PhotoRef":photoURL, u"DateUpdated":dateUpdated}
    db.add_repair(houseAddress, date, repairs)
    
    return ""

@app.route("/GetRepairman", methods=["POST"])
def getRepairsman():
    data= request.get_json(cache=True)
    category = data["category"]
    address = data["houseAddress"]
    API_KEY = 'AIzaSyAZNz6yrGRa698IjwKwtOIEk9Bb4F7fC_Q'
    google_places = GooglePlaces(API_KEY)

    geolocator = Nominatim(timeout=10)
    location = geolocator.geocode(address)

    keywordString=''
    typeToSearch=''
    if (category == 'Electrical'):
        typeToSearch = types.TYPE_ELECTRICIAN
        keywordString = 'electrician'
    if (category == 'Plumbing'):
        typeToSearch = types.TYPE_PLUMBER
        keywordString = 'plumber'
    if (category == 'LockSmituh'):
        typeToSearch = types.TYPE_LOCKSMITH
        keywordString = 'locksmith'

    query_result = google_places.nearby_search(
        lat_lng={'lat': location.latitude, 'lng': location.longitude}, keyword=keywordString,
        radius=20000, types=[typeToSearch])

    jsonSearch = []

    for place in query_result.places:
        try:
            placeName = place.name
            details = place.get_details()
            placeAddress = place.details['formatted_address']
            placeNumber = place.details['formatted_phone_number']
            placeHours = place.details['opening_hours']['weekday_text']
            placeRating = float(place.details['rating'])
            
            repairMan = {'name':placeName, 'number':placeNumber, 'rating':placeRating, 'hours':placeHours, 'address':placeAddress}
            jsonSearch.append(repairMan)
        except:
            continue
    print(jsonSearch)
    jsonData = json.dumps(jsonSearch)
    return jsonData



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)