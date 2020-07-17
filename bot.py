from twitter.auth import create_api


def main():
    # Authenticate to Twitter and create API object
    api = create_api()

    # Create a tweet
    api.update_status("Hello from Tweepy!")


def check_mentions(api, keywords, since_id):
    pass


if __name__ == "__main__":
    main()
