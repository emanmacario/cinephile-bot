import tweepy
from twitter_api_credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def main():
    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print("Authentication successful")
    except Exception as e:
        print("Error during authentication")
        raise e

    # Create a tweet
    api.update_status("Hello from Tweepy!")


if __name__ == "__main__":
    main()