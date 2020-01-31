from FirebaseAdmin import FirebaseAdmin
import datetime

class RatingSystem:


    def __init__(self):
        self._admin = FirebaseAdmin()
        self._db = self._admin.get_db_instance()






    def get_payment_rating(self):
        results = []
        landlordSnapshot = self._db.collection("Landlord").document("rts1234567@hotmail.com").get()
       
        payments = landlordSnapshot.get("payments")
       
        for payment in payments:
            result = {}
            result["house"] = payment["houseAddress"]
            result["tenantName"] = payment["tenantName"]
            dueDate = payment["dueDate"]
            datePaid = payment["datePaid"]
            result["rating"] = self.calc_payment_rating(self.formatPaymentDueDate(dueDate), self.formatPaymentDatePaid(datePaid))
            results.append(result)
        return results
                    
        
      
    def formatPaymentDueDate(self, date):
        strSplit = date.split(" ")
        now = datetime.datetime.now()
        dueDate = datetime.datetime(now.year, self.convert_month_to_number(strSplit[2]), int(strSplit[3]))
        return dueDate

    def formatPaymentDatePaid(self, date):
        strSplit = date.split("-")
        return datetime.datetime(int(strSplit[0]), int(strSplit[1]), int(strSplit[2]))

    def convert_month_to_number(self, monthName):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        for month in months:
            if monthName == month:
                return months.index(month) + 1


    def calc_payment_rating(self, dateDue, datePaid):
        days = dateDue - datePaid
        if days.days >= 7:
            return .1
        if days.days < 7 and days.days >= 0:
            return .05
        else:
            return -.1



rs = RatingSystem()

print(rs.get_payment_rating())