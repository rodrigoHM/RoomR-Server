from google.cloud import translate
from google.auth import credentials
from google.cloud import vision
import os, requests, json

class Prediction():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "pretrainedModel.json"


    def __init__(self, imageURL, language):
        self.imageURL = imageURL
        self.language = language

    def categoryPrediction(self, predictionWord):
        print(predictionWord)
        electricalWords = ["electrician", "copper", "Lighting","Light fixture", "Ceiling", "Lighting accessory", "Light", "flex", "Electrical wiring", "Electronics", "Circuit breaker", "Technology", "outlet","electric outlet","electric receptacle","wall plug","Wall socket"]
        plumbingWords = ["Toilet","Toilet seat", "Bathroom","Plumbing fixture", "Property", "Ceramic", "Sink","Bathroom sink","Bathroom","Washing machine", "Major appliance", "Clothes dryer", "Home appliance", "Laundry room","Laundry"]
        lockSmithWords = ["Wood","Wood stain", "Wall", "Room", "Property", "Door", "knob", "Door handle", "Handle","Lock"]
        category = ""
        for word in electricalWords:
            if(predictionWord == word or category == ""):
                category = "Electrical"
                break
        for word in plumbingWords:
            if(predictionWord == word):
                category = "Plumbing"
                break
        for word in lockSmithWords:
            if(predictionWord == word):
                category = "LockSmith"
                break
        if (category == ""):
            category == "Not Available"
        return category
            
    def getImagePredictionLabel(self):
        predictionData = []
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = self.imageURL

        response = client.label_detection(image=image)
        labels = response.label_annotations

        position = 0
        for label in labels:
            if (label.score >= 0.80):
                position = position + 1
                if(not(label.description == "")):
                    predictionData.append({"label":label.description,"scored":label.score})
                #print('Position: {0}'.format(position))
                print('Label : {0}'.format(label.description))
                #print('Score : {0}'.format(label.score))
        if not predictionData:
            predictionData.append({"error":"Picture Not Accurate Enough Please take picture again"})
        predictionWord = predictionData[0]['label']
        return predictionWord

    def getWordsToOtherLanguage(self,words):
        translate_client = translate.Client()
        target = self.language
        trans = []

        if (self.language != "none"):
            for w in words:
                translation = translate_client.translate(w, target_language=target)

                trans.append(translation["translatedText"])
        else:
            trans.append({"none"})
        return trans


    def getOtherWordsforWord(self, word):
        words = []
        res = requests.get("https://api.datamuse.com/words?ml=" + word + "&topics=electrical&max=4")

        if res.status_code != 200:
            print("Error")
        else:
            for item in res.json():
                words.append(item["word"])
        return words


    def getWordsRelatedToImage(self):
        urlAndTranslations = []
        #data = request.get_json(cache=True)
        #photo = data["photo"]
        #language = data["language"]

        predictionWord = self.getImagePredictionLabel()
        categoryWord = self.categoryPrediction(predictionWord)
        wordsInEnglish = self.getOtherWordsforWord(predictionWord)
        wordsInEnglish.append(predictionWord)
        if self.language == "none":
            wordsInOtherLanguage = "none"
        else:
            wordsInOtherLanguage = self.getWordsToOtherLanguage(wordsInEnglish)
        
        urlAndTranslations.append({'wordsInOtherLanguage': wordsInOtherLanguage})
        urlAndTranslations.append({'imgUrl': self.imageURL})
        urlAndTranslations.append({'wordsInEnglish': wordsInEnglish})
        urlAndTranslations.append({'category': categoryWord})
        jsonData=json.dumps(urlAndTranslations)
        return jsonData