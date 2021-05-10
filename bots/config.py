# tweepy-bots/bots/config.py
import tweepy
import logging
import os
#from google.cloud import translate_v2
import googlemaps

logger = logging.getLogger()

def twitter_api():
    consumer_key = os.getenv("API_KEY")
    consumer_secret = os.getenv("API_SECRET_KEY")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


# def translate_api():
#     creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
#     translater = translate_v2.Client.from_service_account_json(creds)
#     return translater

def places_api():
    key =  os.getenv("GOOGLE_PLACES_API_KEY")
    retriever = googlemaps.Client(key=key)
    return retriever