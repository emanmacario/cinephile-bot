#!/usr/bin/env python
import json
import logging
import time
import tweepy
from tmdb.search import get_movie, search_for_movie
from twitter.auth import create_api

# Development imports
from pprint import pprint

"""
Tweet objects: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
User objects: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
"""

"""
TODO: Exception handling
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, keywords, since_id):
    logger.info('Retrieving mentions')
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        print("="*50)
        print(tweet)
        print(tweet.text)
        #pprint(tweet._json.keys())

        hashtags = tweet.entities['hashtags']

        print(hashtags)
        new_query = False
        for hashtag in hashtags:
            if hashtag['text'] == 'movie':
                print("Indicies: ", hashtag['indices'])
                index = hashtag['indices'][1] + 1
                print(f"Movie: '{tweet.text[index:]}'")
                movie = tweet.text[index:]
                new_query = True
                break


        new_since_id = max(tweet.id, new_since_id)

        # Tweet is ignored if it is a reply to another tweet
        if tweet.in_reply_to_status_id is not None:
            continue

        if new_query:
            response = search_for_movie(movie)
            print("Total results: ", len(response['results']))
            # pprint(response['results'][0])
            top_result = response['results'][0]
            movie_id = top_result['id']

            response = get_movie(movie_id)
            # pprint(response)
            extract_info(response)


        # if any(keyword in tweet.text.lower() for keyword in keywords):
        #     logger.info(f"Answering to @{tweet.user.screen_name}")

            # id1 = api.update_status(
            #     status=f"@{tweet.user.screen_name} Please reach us via DM lol",
            #     in_reply_to_status_id=tweet.id
            # )

            # id2 = api.update_status(
            #     status=f"@{tweet.user.screen_name} yeah true please do that",
            #     in_reply_to_status_id=id1
            # )
    return new_since_id



def extract_info(response):
    """
    Extracts key information from primary information given in the JSON response object
    :param response: response JSON object
    :return: dictionary
    """
    """
    === TWEET #1 ===
    1. Release Date
    2. Time
    3. Star rating
    4. Budget and gross (with percentage)
    5. Genres
    6. Production countries
    
    === TWEET #2 ===
    1. Director
    2. Written by
    3. Starring
    
    === Tweet #3 ===
    1. Description
    """
    # NB: Could do something like { k: v for k, v in dict.items() if k in keys }

    # Tweet #1
    original_title = response['original_title']
    release_date = response['release_date']
    runtime = response['runtime']
    vote_average = response['vote_average']
    budget = response['budget']
    revenue = response['revenue']
    genres = [genre['name'] for genre in response['genres']]
    production_countries = [country['iso_3166_1'] for country in response['production_countries']]
    print(original_title)
    print(release_date)
    print(runtime)
    print(vote_average)
    print(budget)
    print(revenue)
    print(genres)
    print(production_countries)

    # Tweet #2
    get_credits(response)

    # Tweet #3
    overview = response['overview']
    print("OVERVIEW:")
    print(overview, '\n')

    # Extra
    poster_path = response['poster_path']
    backdrop_path = response['backdrop_path']
    print(f"Poster path: {poster_path}")
    print(f"Backdrop path: {backdrop_path}")



def get_credits(response):
    """
    Extracts credit information (e.g. Directors, actors, writers)
    :param response: JSON response object
    :return: dictionary
    """
    credits = response['credits']
    cast = credits['cast']
    crew = credits['crew']

    # Get top five actors and/or actresses
    actors = [person['name'] for person in cast[:5]]
    print("STARRING:")
    pprint(actors)

    # Get director(s)
    print("DIRECTED BY:")
    directors = [person['name'] for person in crew if person['job'] == 'Director']
    pprint(directors)

    # Get writer(s)
    writers = [person['name'] for person in crew if person['job'] == 'Writer']
    pprint("WRITTEN BY:")
    pprint(writers)


def main():
    # Authenticate to Twitter and create API object
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ['help', 'support'], since_id)
        logger.info('Waiting...')
        time.sleep(60)


def reply_to_user(screen_name, in_reply_to_status_id, movie_name):
    search_for_movie(movie_name)


def reply_to_self():
    api = create_api()
    status = api.update_status('Hello joe')

    reply_id = status.id
    screen_name = status.user.screen_name
    api.update_status(f'@{screen_name} Hello, just replying to myself!', in_reply_to_status_id=reply_id)


if __name__ == "__main__":
    main()