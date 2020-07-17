import tweepy
import logging
import os
from dotenv import load_dotenv, find_dotenv

# Set logger
logger = logging.getLogger()

# Load Twitter API keys and credentials
load_dotenv(find_dotenv())
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


def create_api():
    """
    Authenticates application to the Twitter API
    and returns an API object for interfacing with
    the Twitter API
    :return: API object
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API successfully created")

    return api


def main():
    api = create_api()


if __name__ == "__main__":
    main()
