import requests
import hashlib
import calendar
import time


from api.MarvelComics import Config
from pages.models import Characters, Comics

base_url = "http://gateway.marvel.com/"
gt = time.gmtime()
ts = calendar.timegm(gt)
hash = hashlib.md5((str(ts) + Config.privKey + Config.pubKey).encode())

class Marvel():
    def getCharacter(self, name):

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
            characterDesc = ""
            #Gets the character description(If there is one)
            if (characterData[0].get("description") == ""):
                characterDesc = "This character has no description sadly."
            else:
                characterDesc = characterData[0].get("description")
                print(characterDesc)

            #Gets the character image(If there is one)
            imageExtension = characterData[0].get("thumbnail").get("extension")
            characterImage = characterData[0].get("thumbnail").get("path") + "." + imageExtension
        
            #This checks for if the character name is already in the database, if it is it does nothing, if it doesn't it'll save that character into the database.    
            x = Characters.objects.filter(name=characterName).exists()
            if (x):
                print("This character is already in the database")
            else:
                c = Characters(name=characterName, characterId=characterID, characterImage=characterImage, characterDescription=characterDesc)
                c.save()
            print(characterName)        
            print(characterImage)

        return characterName, characterImage, characterID, characterDesc

    #Add more variables into the function to access the startYear search and any other variables that are put into the PARAMS in the future
    def getComics(self, character, *args):
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
            buyLink = ""
            #Goes through the results length
            for i in range(len(comicData)):
               
               #Searches through urls to get the link for purchasing the comic
                charUrl = comicData[i].get("urls")
                for url in charUrl:
                    if url['type'] == 'purchase':
                        buyLink = url['url']                

                #Gets ComicID equal to the range value (Should get the comicID)
                comicIDE = comicData[i].get("id")
                print(comicIDE)

                #Gets the comic title
                comicTitle = comicData[i].get("title")
                #print(comicTitle)s

                comicYears = ""
                #Should get the comic date from the title
                for m in comicTitle:
                    if m.isdigit():
                        if (len(comicYears)) == 4:
                            pass
                        else:
                            comicYears += m
                
                newcomicYears = int(comicYears)
                print(newcomicYears)

                #Gets comic description for that comic
                comicDesc = comicData[i].get("description")
                print(comicDesc)
                #Gets comic book authors/writers
                if comicData[i].get("creators").get("available") == 0:
                    comicAuthors = "This comic has an unknown writer/author"
                else:
                    authors = comicData[i].get("creators").get("items")
                    comicAuthors = [x['name'] for x in authors]
                    

                #Gets comic book image
                imageExtension = comicData[0].get("thumbnail").get("extension")
                comicImage = comicData[0].get("thumbnail").get("path") + "." + imageExtension

                print(comicAuthors, "\n", comicImage + "\n" + buyLink)
                x = Comics.objects.filter(comicID=comicIDE).exists()
                if (x):
                    print("This comic is already in the database!")
                else:
                    c = Comics(title= comicTitle, summary=comicDesc, linkForPurchase=buyLink, comicIMG=comicImage, comicID=comicIDE, comicYear = newcomicYears)
                    c.save()
    #This will test the function getCharacter()
    #getCharacter("Thor")

    #This one tests the function getComics()
    #getComics(1009351, 1999)

