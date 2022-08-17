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
            text = 'Ist dieses Fahrrad-Problem noch aktuell? '+pickedRecord['description'] + ' ' +pickedRecord['url']
        case 'solved_bike':
            text = 'Diese Problemstelle für Fahrräder wurde als behoben markiert. Wie findest du das? '+pickedRecord['description'] + ' ' +pickedRecord['url']
        case 'problem_side_walk':
            text = 'Ist dieses Gehweg-Problem noch aktuell? '+pickedRecord['description'] + ' ' +pickedRecord['url']
        case 'solved_side_walk':
            text = 'Diese Problemstelle für Gehwege wurde als behoben markiert. Wie findest du das? '+pickedRecord['description'] + ' ' +pickedRecord['url']

    return text

# Call the API
response = request()

# Parse the JSON response
data = json.loads(response.read())

# Use local JSON test data file
# f = open('lots.json',  encoding='utf-8')
# data = json.load(f)

# Print lots of texts for debugging purposes

# Finaly run the main loop
while True:
    text = createRandomTextFromJson(data)
    print("Sending text to Twitter: "+text)
    #response = tweetText(text)
    #print(response)
    oneHour = 1*60*60
    sleepTimeSeconds = randrange(oneHour*3, oneHour*6)
    sleepTimeHours = sleepTimeSeconds / 60 / 60
    print("Sleeping "+str(sleepTimeSeconds)+" seconds ("+str(sleepTimeHours)+" hours) ...");
    # Do not forget to flush the output buffer and print it on the screen because of sleep
    sys.stdout.flush()
    time.sleep(sleepTimeSeconds);
