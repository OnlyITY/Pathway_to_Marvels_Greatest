import requests
import hashlib
import calendar
import time

from api.MarvelComics import Config
from pages.models import Characters, Comics

base_url = "http://gateway.marvel.com/"
URL = "http://gateway.marvel.com/v1/public/characters"

gt = time.gmtime()
ts = calendar.timegm(gt)

hash = hashlib.md5((str(ts) + Config.privKey + Config.pubKey).encode())

def getCharacter(name):

    query = base_url + "v1/public/characters"
    PARAMSS = {
        "apikey": Config.pubKey,
        "ts": ts,
        "hash" : hash.hexdigest(),
        "name": name
    }   

    #Opens up the url using the parameters given to search for the inputted character
    r = requests.get(url = query, params=PARAMSS)

    #Turns the requested data into a json and saved into a variable
    data = r.json()

    if len(data.get("data").get("results")):
        noImage = False
        #Searches through the data under the results
        characterData = data.get("data").get("results")

        #Gets the character's urls
        characterURLS = characterData[0].get("urls")

        #Gets character ID
        characterID = characterData[0].get("id")
        #Gets the character name
        characterName = characterData[0].get("name")

        #Gets the character description(If there is one)
        if (characterData[0].get("description") == ""):
            print("This character has no description sadly.")
            noImage = True
        else:
            characterDesc = characterData[0].get("description")
            print(characterDesc)

        #Gets the character image(If there is one)
        imageExtension = characterData[0].get("thumbnail").get("extension")
        characterImage = characterData[0].get("thumbnail").get("path") + "." + imageExtension

        c = Characters(name=characterName, characterId=characterID, characterImage=characterImage, characterDescription=characterDesc)
        c.save()
        print(characterName)        
        print(characterImage)

        if(noImage == True):
            return characterName, characterImage, characterID
        else:
            return characterName, characterImage, characterDesc, characterID

#Add more variables into the function to access the startYear search and any other variables that are put into the PARAMS in the future
def getComics(character, *args):
    query = base_url + "v1/public/comics"

    PARAMS = {
        "apikey": Config.pubKey,
        "ts": ts, 
        "hash" : hash.hexdigest(),
        "characters": character,
        "startYear": args,

    }   

    r = requests.get(url = query, params=PARAMS)

    data = r.json()

    if len(data.get("data").get("results")):
        #Makes comicData equal to the results section
        comicData = data.get("data").get("results")

        #Goes through the results length
        for i in range(len(comicData)):

            #Gets ComicID equal to the range value (Should get the comicID)
            comicID = comicData[i].get("id")
            print(comicID)
            #Gets the comic title
            comicTitle = comicData[i].get("title")
            #print(comicTitle)

            #Gets the comic year (This doesn't work because the place it searches doesn't give the comic year
            comicYear = comicData[i].get("Year")

            #Gets comic book authors/writers
            if comicData[i].get("creators").get("available") == 0:
                comicAuthors = "This comic has an unknown writer/author"
            else:
                comicAuthors = comicData[i].get("creators").get("items")

            #Gets comic book image
            imageExtension = comicData[0].get("thumbnail").get("extension")
            comicImage = comicData[0].get("thumbnail").get("path") + "." + imageExtension

            print(comicAuthors, "\n", comicImage)
#This will test the function getCharacter()
getCharacter("Thor")

#This one tests the function getComics()
#getComics(1009368, 1999)
