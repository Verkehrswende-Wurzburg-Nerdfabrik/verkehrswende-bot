# import general stuff
from urllib.request import urlopen, Request
from random import *
import json
import sys
import time

# import twitter stuff
import tweepy
import botConfig


# Function to tweet/text
def tweetText(tweetString):
      client = tweepy.Client(consumer_key=botConfig.consumer_key,
                       consumer_secret=botConfig.consumer_secret,
                       access_token=botConfig.access_token,
                       access_token_secret=botConfig.access_token_secret)

      response = client.create_tweet(text=tweetString)
      return response

# Lets define a function for requesting the API
def request():
    #get the data via API
    #set some parameter for request to simulate a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    req_url = "https://www.verkehrswende-wuerzburg.de/api/locations"
    req = Request(url=req_url, headers=headers)
    #store the response of URL
    response = urlopen(req)
    return response

def createRandomTextFromJson(records):

    # pick a random key from the record list
    randomKey = choice(list(records))

    # Get the record data
    pickedRecord = records[randomKey]

    # print(pickedRecord)

    text = ''

    match pickedRecord['type']:
        case 'problem_bike':
            text = pickedRecord['title'] + ': Bitte hilf mir dabei Problemstellen für den Verkehr in #Würzburg aktuell zu halten. Ist dieses Fahrrad-Problem noch aktuell? Gibt es neue Bilder dieser Stelle? '+pickedRecord['url']
        case 'solved_bike':
            text = pickedRecord['title'] + ': Bitte hilf mir dabei positive Beispiele für die Verkehrswende in #Würzburg aktuell zu halten. Ist diese Stelle für Fahrrader noch immer ein positives Beispiel? Gibt es neue Bilder dieser Stelle? '+pickedRecord['url']
        case 'problem_side_walk':
            text = pickedRecord['title'] + ': Bitte hilf mir dabei Problemstellen für den Verkehr in #Würzburg aktuell zu halten. Ist dieses Gehweg-Problem noch aktuell?  Gibt es neue Bilder dieser Stelle? '+pickedRecord['url']
        case 'solved_side_walk':
            text = pickedRecord['title'] + ': Bitte hilf mir dabei positive Beispiele für die Verkehrswende in #Würzburg aktuell zu halten. Ist diese Stelle für Fußgänger:innen noch immer ein positives Beispiel? Gibt es neue Bilder dieser Stelle? '+pickedRecord['url']
    return text

# Finaly run the main loop
while True:
    response = request()
    data = json.loads(response.read())
    text = createRandomTextFromJson(data)
    print("Sending text to Twitter: "+text)
    response = tweetText(text)
    print(response)
    daysInSeconds = 1*60*60*24*3
    sleepTimeDays = daysInSeconds / 24 / 60 / 60
    print("Sleeping "+str(daysInSeconds)+" seconds ("+str(sleepTimeDays)+" days) ...");
    # Do not forget to flush the output buffer and print it on the screen because of sleep
    sys.stdout.flush()
    time.sleep(daysInSeconds);
