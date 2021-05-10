# Polybot

## Purpose

This is a project for Data Science Systems (DS 3002) at UVA. This is a Twitter bot that will give you the current weather details of the location your tweet or any U.S. city,  and 7 random restaurants from your location and their details. This bot retrieves tweets from its mentions every 20 seconds, so you may have to wait at most 20 seconds for a repsonse. *Unfortunately, grpcio is failing to build with the rest of the project, sothe translation feature is not active right now.*

The Twitter bot is @Andrew31621328.

## How It Works

Using APIs from Google, Twitter, and OpenWeather, this bot can do a variety of things. It was coded in Python and then containerized in Docker and deployed to an AWS EC2 instance. To use the bot, tweet at it with one of the valid statements and it will DM you a response depending on what you said.

## How to Use the Code

This bot is deployed to an EC2 instance. You can just tweet at the bot now and it will return DMs to your Twitter account.

If you want to build it in Docker yourself, download Docker if you haven't already and then continue below.

Download the code and the Dockerfile. This bot uses the Twitter API, Google Places API, and OpenWeather API. You will need to create a Twitter Developer Account for the Twitter API, a Google Cloud Platform (GCP) account for the Google Places API, and an OpenWeather account for the OpenWeather API. 

Twitter has a consumer key, secret consumer key, token, and secret token. Get all 4 of those. 

For Google, login to your GCP account and search for Places API. Enable it and then go to Navigation Menu -> APIs & Services -> Credentials. Click on Create Credentials -> API Key. Now you have an API key to use. 

OpenWeather only has one key to get. After you collect all the necessary keys do one of the following:

Follow the instructions in the **Using Tweepy** section in this article https://realpython.com/twitter-bot-python-tweepy/. You will be able to install Tweepy and make a virtual environment. Then:

### Option 1:

1. The DockerFile has dummmy inputs for all the keys. Put each one of your keys in the correct environment variable in the DockerFile. The first four belong to your Twitter Keys, the next one is where you put your OpenWeather key, and the last is Google Places API's key. Fill in those values with your keys and you can run it locally.

2. Type **docker build . -t polybot** to build

3. Type **docker run -it polybot** to run

### Option 2:

1. Type **docker build .-t polybot** to build

2. Type **docker run -it -e API_KEY="YourTwitterAPIKey" \
  -e API_SECRET_KEY="YourTwitterAPISecretKey" \ 
  -e ACCESS_TOKEN="YourTwitterToken" \
  -e ACCESS_TOKEN_SECRET="YourTwitterSecretToken" \
  -e OPEN_WEATHER_KEY="YourOpenWeatherKey" \
  -e GOOGLE_PLACES_API="YourPlacesAPIKey" polybot**

This should make the bot active and you can test things out.


## Everything it can do (minus translation):

- Tweet "help" or "info" at it to make polybot give you a rundown of its functions
- Tweet "hi", "hey", "hello", or "howdy" and polybot will say hi back
- Tweet "How many times have you been used?" and polybot will reply with the number of people he has helped.
- Tweet "who made you" and polybot will respond with an answer
- Tweet "what's the weather" or "weather" with your location on and polybot will DM you details about the current weather in your location
- Tweet "what's the weather in <location>" and polybot will DM you details about the current weather in <location>
- Tweet "coat" or "jacket" and polybot will respond with if you need a coat or jacket
- Tweet "umbrella" and polybot will respond with if you need an umbrella
- Tweet something with "restaurants" and "nearby" or "near" and "me" and polybot will give you 7 random restaurants in your location and their details



