#!/usr/bin/env python
# tweepy-bots/bots/polybot.py

import logging
import requests
import os
from config import twitter_api, places_api
import time
import tweepy
import googlemaps
import random
#from google.cloud import translate_v2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    answers = 0

    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)

        if tweet.in_reply_to_status_id is not None:
            continue
        
        ## Replies ##

        # original form
        orig_message = tweet.text
        # full lowered form
        tw_message = tweet.text.lower()
        # list form lowered
        twit = tw_message.split()
        # list form orig
        orig_twit = orig_message.split()
        # user
        user = api.get_user(tweet.user.id)
        # No username
        test = " ".join(twit[1:])
        
        try:

            ####### CONVERSATIONAL PART ########
            if ("hi" in test) or ("hello" in test) or ("hey" in test) or ("howdy" in test):
                api.send_direct_message(
                    recipient_id=tweet.user.id, 
                    text=("Hi " + user.screen_name + "!")
                    )
            
            elif (test == "how many times have you been used?") or (test == "how many times have you been used"):
                answers += 1
                if answers == 1:
                    api.send_direct_message(
                        recipient_id=tweet.user.id, 
                        text=("I've been used " + str(answers) + " time!")
                        )

                else:
                    api.send_direct_message(
                        recipient_id=tweet.user.id, 
                        text=("I've been used " + str(answers) + " times!")
                        )
            
            elif (test == "who made you?") or (test == "who made you"):
                api.send_direct_message(
                    recipient_id=tweet.user.id, 
                    text=("Mr. beep")
                    )
            ####### TRANSLATION ####### 
            # if twit[1] == "translate":
            #     logger.info(f"Answering to {tweet.user.name}")
            #     # Get Google Translate
            #     translater = translate_api()
            #     languages = True
                
            #     # Get the text to be translated
            #     text = " ".join(twit[2:-2])
            #     orig_text = " ".join(orig_twit[2:-2])

            #     # Get Language and language Code
            #     target_lang = twit[-1]
            #     lang = ''

            #     if languages: 
            #         if target_lang == "japanese":
            #             lang = 'ja'
            #         elif target_lang == "spanish":
            #             lang = 'es'
            #         elif target_lang == "dutch":
            #             lang = 'nl'
            #         elif target_lang == "portuguese":
            #             lang = 'pt'
            #         elif target_lang == "german":
            #             lang = 'de'
            #         elif target_lang == "arabic":
            #             lang = 'ar'
            #         elif target_lang == "french":
            #             lang = 'fr'
            #         elif target_lang == "italian":
            #             lang = 'it'
            #         elif target_lang == "korean":
            #             lang = 'ko'
            #         elif target_lang == "russian":
            #             lang = 'ru'
            #         elif target_lang == "norwegian":
            #             lang = 'no'
            #         elif target_lang == "swedish":
            #             lang = 'sv'
            #         elif target_lang == "persian":
            #             lang = 'fa'
            #         elif target_lang == "finnish":
            #             lang = 'fi'
            #         elif target_lang == "filipino":
            #             lang = 'fil'
            #         elif target_lang == "hindi":
            #             lang = 'hi'
            #         elif target_lang == "turkish":
            #             lang = 'tr'
            #         elif target_lang == "chinesesi":
            #             lang = 'zh-CN'
            #         elif target_lang == "chinesetr":
            #             lang = 'zh-TW'
            #         elif target_lang == "thai":
            #             lang = 'th'
            #         elif target_lang == "urdu":
            #             lang = 'ur'
            #         elif target_lang == "vietnamese":
            #             lang = 'vi'

            #     output = translater.translate(text, target_language=lang)
            #     translation = "@" + user.screen_name + " " + orig_text + " in " + target_lang.title() + " is: " + output["translatedText"]

            #     api.send_direct_message(
            #         recipient_id=tweet.user.id,
            #         text=translation,
            #     )
            
            ####### WEATHER ####### 
            ## Current Weather From Tweet Location
            if test == "what’s the weather" or test == "what’s the weather?" or test == "weather" or ("weather" in test and "translate" not in test):
                try:
                    logger.info(f"Answering to {tweet.user.name}")

                    key = os.getenv("OPEN_WEATHER_KEY")
                    location = tweet.place.name

                    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}"
                    response = requests.get(url).json()

                    condition = response["weather"][0]["main"]
                    
                    farenheit =  (float(response["main"]["temp"]) - 273.15) * 9/5 + 32
                    feels = (float(response["main"]["feels_like"]) - 273.15) * 9/5 + 32
                    milesper = float(response['wind']["speed"]) * 2.237
                    humidity = float(response["main"]["humidity"])

                    if float(response['wind']["speed"]) > 348.75 or float(response['wind']["speed"]) <= 11.25:
                        direction = "north"
                    elif float(response['wind']["speed"]) > 11.25 and float(response['wind']["speed"]) <= 78.75:
                        direction = "northeast"
                    elif float(response['wind']["speed"]) > 78.75 and float(response['wind']["speed"]) <= 101.25:
                        direction = "east"
                    elif float(response['wind']["speed"]) > 101.25 and float(response['wind']["speed"]) <= 168.75:
                        direction = "southeast"
                    elif float(response['wind']["speed"]) > 168.75 and float(response['wind']["speed"]) <= 191.25:
                        direction = "south"
                    elif float(response['wind']["speed"]) > 191.25 and float(response['wind']["speed"]) <= 258.75:
                        direction = "southwest"
                    elif float(response['wind']["speed"]) > 258.75 and float(response['wind']["speed"]) <= 281.25:
                        direction = "west"
                    elif float(response['wind']["speed"]) > 281.25 and float(response['wind']["speed"]) <= 348.75:
                        direction = "northwest"

                    api.send_direct_message(
                        recipient_id=tweet.user.id, 
                        text=("Right now, it is " + condition.lower() + " and it is " + str(round(farenheit, 1)) + " degrees, but it feels like " + str(round(feels, 1)) + " degrees in " + response["name"] + "." +
                        " \nThe wind is blowing " + direction + " at " + str(round(milesper,3)) + " miles per hour." +
                        " \nThe humidity is " + str(humidity) + "%.")
                        )

                except:
                    api.send_direct_message(
                        recipient_id=tweet.user.id, 
                        text=("I can't seem to get your location, is your tweet location on?")
                        )

            
            ## Current weather in a locaion not from the tweet
            elif ("in" in test and "weather" in test) and "translate" not in test:
                logger.info(f"Answering to {tweet.user.name}")

                key = os.getenv("OPEN_WEATHER_KEY")
                tempr = test.split()
                after = tempr.index("in")

                # For multi word locations
                if len(tempr[after+1:]) > 1:
                    loc = ""
                    for i in range(len(tempr[after+1:])):
                        if i != len(tempr[after+1:]) - 1:
                            loc += tempr[after+1:][i] + "+"
                        else:
                            tempr[-1] = tempr[-1].strip("?")
                            loc += tempr[after+1:][i]
                else:
                    # For single word locations
                    if "?" in tempr[-1]:
                        tempr[-1] = tempr[-1].strip("?")
                        loc = " ".join(tempr[after+1:])
                    else:
                        loc = " ".join(tempr[after+1:])

                try:
                    url = f"https://api.openweathermap.org/data/2.5/weather?q={loc}&appid={key}"
                    response = requests.get(url).json()

                    condition = response["weather"][0]["main"]
                    
                    farenheit =  (float(response["main"]["temp"]) - 273.15) * 9/5 + 32
                    feels = (float(response["main"]["feels_like"]) - 273.15) * 9/5 + 32
                    milesper = float(response['wind']["speed"]) * 2.237
                    humidity = float(response["main"]["humidity"])

                    if float(response['wind']["speed"]) > 348.75 or float(response['wind']["speed"]) <= 11.25:
                        direction = "north"
                    elif float(response['wind']["speed"]) > 11.25 and float(response['wind']["speed"]) <= 78.75:
                        direction = "northeast"
                    elif float(response['wind']["speed"]) > 78.75 and float(response['wind']["speed"]) <= 101.25:
                        direction = "east"
                    elif float(response['wind']["speed"]) > 101.25 and float(response['wind']["speed"]) <= 168.75:
                        direction = "southeast"
                    elif float(response['wind']["speed"]) > 168.75 and float(response['wind']["speed"]) <= 191.25:
                        direction = "south"
                    elif float(response['wind']["speed"]) > 191.25 and float(response['wind']["speed"]) <= 258.75:
                        direction = "southwest"
                    elif float(response['wind']["speed"]) > 258.75 and float(response['wind']["speed"]) <= 281.25:
                        direction = "west"
                    elif float(response['wind']["speed"]) > 281.25 and float(response['wind']["speed"]) <= 348.75:
                        direction = "northwest"

                    api.send_direct_message(
                        recipient_id=tweet.user.id, 
                        text=("Right now, it is " + condition.lower() + " and it is " + str(round(farenheit, 1)) + " degrees, but it feels like " + str(round(feels, 1)) + " degrees in " + response["name"] + "." +
                        " \nThe wind is blowing " + direction + " at " + str(round(milesper,3)) + " miles per hour." +
                        " \nThe humidity is " + str(humidity) + "%.")
                        )
                except:
                    api.send_direct_message(
                        recipient_id=tweet.user.id, 
                        text=("Sorry, I don't think that location exists or I can't seem to locate it!")
                        )

            # Should you bring a coat
            if (("coat" in test) or ("jacket" in test)) and "translate" not in test: 
                try:
                    logger.info(f"Answering to {tweet.user.name}")

                    key = os.getenv("OPEN_WEATHER_KEY")
                    location = tweet.place.name

                    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}"
                    response = requests.get(url).json()
                    
                    temp =  (float(response["main"]["temp"]) - 273.15) * 9/5 + 32
                    feels = (float(response["main"]["feels_like"]) - 273.15) * 9/5 + 32

                    if temp <= 57:
                        api.send_direct_message(
                            recipient_id=tweet.user.id, 
                            text=("Right now, it is " + str(round(temp, 1)) + " degrees, but it feels like " + str(round(feels, 1)) + "." +
                            " \n I would recommend bringing a coat! Brrrr!")  
                        )
                    elif temp > 57 and temp < 75:
                        api.send_direct_message(
                            recipient_id=tweet.user.id, 
                            text=("Right now, it is " + str(round(temp, 1)) + " degrees, but it feels like " + str(round(feels, 1)) + "." +
                            " \n It is up to you at this temperature! Good temperature for a run!")  
                        )
                    else:
                        api.send_direct_message(
                            recipient_id=tweet.user.id, 
                            text=("Right now, it is " + str(round(temp, 1)) + " degrees, but it feels like " + str(round(feels, 1)) + "." +
                            " \n No need for a coat! Don't burn!")  
                        )
                    
                except:
                        api.send_direct_message(
                            recipient_id=tweet.user.id, 
                            text=("I can't seem to get your location, is your tweet location on?")  
                        )


            # Should you bring an umbrella
            if ("umbrella" in test) and ("translate" not in test):
                try:
                    logger.info(f"Answering to {tweet.user.name}")

                    key = os.getenv("OPEN_WEATHER_KEY")
                    location = tweet.place.name

                    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}"
                    response = requests.get(url).json()

                    condition = response["weather"][0]["main"]

                    if condition != "Rain":
                        api.send_direct_message(
                            recipient_id=tweet.user.id, 
                            text=("No need for an umbrella!")  
                        )
                    else:
                        api.send_direct_message(
                            recipient_id=tweet.user.id, 
                            text=("I would recommend bringing an umbrella!")  
                        )
                
                except:
                    api.send_direct_message(
                            recipient_id=tweet.user.id, 
                            text=("I can't seem to get your location, is your tweet location on?")  
                        )


            ####### RESTAURANTS IN THE LOCATION OF TWEET ########
            elif (("nearby" in test and "restaurants" in test) or (("near" in test and " me " in test) or ("near" in test and " me" in test) or ("near" in test and " me?" in test))) and ("translate" not in test):
                
                try:
                    logger.info(f"Answering to {tweet.user.name}")

                    key = os.getenv("OPEN_WEATHER_KEY")
                    location = tweet.place.name

                    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={key}"
                    response = requests.get(url).json()

                    lon = response["coord"]["lon"]
                    lat = response["coord"]["lat"]
                    insert_coords = str(lat) + "," + str(lon)

                    gmaps = places_api()

                    result = gmaps.places_nearby(location=insert_coords, radius=30000, type = 'restaurant')

                    random.shuffle(result["results"])
                    
                    just_7 = 0
                    say = ""

                    for restaurant in result["results"]:
                        name = restaurant["name"]
                        rating = restaurant['rating']
                        num_ratings = restaurant["user_ratings_total"]
                        vicinity = restaurant["vicinity"]

                        try:
                            if restaurant["opening_hours"]["open_now"] == False:
                                opn = 'is not'
                            else:
                                opn = 'is'
                            
                            try:
                                if restaurant["price_level"] == 0:
                                    price = "free"
                                elif restaurant["price_level"] == 1:
                                    price = "inexpensive"
                                elif restaurant["price_level"] == 2:
                                    price = "moderately priced"
                                elif restaurant["price_level"] == 3:
                                    price = "expensive"
                                elif restaurant["price_level"] == 4:
                                    price = "very expensive"

                                
                                say += ("\n" + name + " has an average rating of " + str(rating) + " given by " + str(num_ratings) + " people!" +
                                        " \nYou can expect this restaurant to be " + price + "!" +
                                        " \nIt " + opn + " open right now." +
                                        " \nThis is located near " + vicinity + ".\n")
                            
                            except:
                                say += ("\n" + name + " has an average rating of " + str(rating) + " given by " + str(num_ratings) + " people!" +
                                        " \nIt " + opn + " right now." +
                                        " \nThis is located near " + vicinity + ".\n")
                        
                        except:
                            try:
                                if restaurant["price_level"] == 0:
                                    price = "free"
                                elif restaurant["price_level"] == 1:
                                    price = "inexpensive"
                                elif restaurant["price_level"] == 2:
                                    price = "moderately priced"
                                elif restaurant["price_level"] == 3:
                                    price = "expensive"
                                elif restaurant["price_level"] == 4:
                                    price = "very expensive"

                                
                                say += ("\n" + name + " has an average rating of " + str(rating) + " given by " + str(num_ratings) + " people!" +
                                        " \nYou can expect this restaurant to be " + price + "!" +
                                        " \nThis is located near " + vicinity + ".\n")
                            
                            except:
                                say += ("\n" + name + " has an average rating of " + str(rating) + " given by " + str(num_ratings) + " people!" +
                                        " \nThis is located near " + vicinity + ".\n")
                        
                        just_7 += 1

                        if just_7 == 7:
                            break
                
                    api.send_direct_message(
                        recipient_id=tweet.user.id, 
                        text=("Here are some restaurants in your city: \n" + say)  
                    )
            
                    
                except:
                    api.send_direct_message(
                        recipient_id=tweet.user.id, 
                        text=("I can't seem to get any restaurants in your location! Maybe wait until you get somewhere else to try again. Make sure your location is on when you tweet!")  
                    )



            ####### HELP #######
            elif twit[1] == "help" or twit[1] == "info":
                if not tweet.user.following:
                        tweet.user.follow()
                
                api.send_direct_message(
                    recipient_id=tweet.user.id, 
                    text=("Hi " + user.screen_name + "!" + 
                    " Unfortunately, my translation feature is broken, but if it weren't:" +
                    " My first function is translation! If you tweet at me like 'Translate <text> to <language>'," + 
                    " then I will translate your text to the target language." +
                    " \n The languages I support are: Spanish, Dutch, German, French, Italian, Russian, Finnish, Swedish," +
                    " Turkish, Arabic, Persian, Hindi, Urdu, Japanese, Korean, Chinese (Simplified), Chinese (Traditional)" +
                    " Thai, Vietnamese, and Filipino!" +
                    " To get Chinese Traditional type Chinesetr and to get Chinese Simplified type Chinesesi." +
                    " \nExample Tweet: @bot Translate Hi I like soccer to French" +
                    "\n" +
                    "\nMy second functionality is getting the current weather for your location or another!" +
                    " \nIf you ask 'What's the weather?' or just 'weather', then I will give you details about " +
                    " the current weather in your location. Make sure you geotag your tweet though. Otherwise " + 
                    " you will need to ask 'What's the weather in <location>?' to get deatils of weather." + 
                    " \nI also tell you if you currently need a coat or umbrella if you mention it in your tweet!" +
                    " \nMy third functionality is retrieving restaurants in your tweet location! I will give you 7 random choices and deatils about each one." +
                    " Just say 'restaurants nearby' or 'near me' and make sure your tweet location is on!")
                    )
            
            answers += 1

        except:
             api.send_direct_message(
                    recipient_id=tweet.user.id, 
                    text=("Sorry, I don't know that command! Tweet help or info at me for my functionality!")
                    )

    return new_since_id

def main():
    api = twitter_api()
    since_id = 1
    keywords = ["help", "info", "translate"]
    while True:
        since_id = check_mentions(api, keywords, since_id)
        logger.info("Waiting...")
        time.sleep(20)

if __name__ == "__main__":
    main()