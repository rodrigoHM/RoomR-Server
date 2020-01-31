import datetime

class RepairRating:
    def __init__(self, datePosted, dateUpdated, LandlordEmail):
        self._datePosted = datePosted
        self._dateUpdated = dateUpdated
        self._LandlordEmail = LandlordEmail
        self._dateFormat = ""

    def setDateUpdated(self, updateString):
        self._dateUpdated = updateString

    def getDateUpdated(self):
        return self._dateUpdated

    def calculateRating(self):
        dateStringSplit = self._datePosted.split(" ")
        dateUpdatedStringSplit = self._dateUpdated.split(" ")

        dateUpdatedStringSplit = dateUpdatedStringSplit[0].split("-")
        dateStringSplit = dateStringSplit[0].split("-")
        
        #[year,month,day]
        dateUpdatedPrep = datetime.date(int(dateUpdatedStringSplit[0]),int(dateUpdatedStringSplit[1]), int(dateUpdatedStringSplit[2]))
        datePostedPrep = datetime.date(int(dateStringSplit[0]), int(dateStringSplit[1]),int(dateStringSplit[2]))

        month = ""
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        for i in range(len(months)):
            if ((i+1) == dateUpdatedPrep.month):
                month = months[i]
        newStringDate = str(month) + " " + str(dateUpdatedPrep.year)
        self.setDateUpdated(newStringDate)
        print(self._dateUpdated)
        
        days = datePostedPrep - dateUpdatedPrep
        if days.days >= 7:
            return -.1
        if days.days < 7 and days.days >= -0.01:
            return .1
        else:
            return -.2
