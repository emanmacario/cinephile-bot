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
            info = extract_info(response)
            # pprint(info)
            reply_to_user(info)


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



def extract_info(movie):
    """
    Extracts key information from primary information given in the JSON response object
    :param movie: response JSON object
    :return: dictionary
    """
    # Keys for tweets
    keys = ('original_title',
            'release_date',
            'runtime',
            'vote_average',
            'budget',
            'revenue',
            'overview',
            'poster_path',
            'backdrop_path')

    # Tweet #1
    info = {key: value for key, value in movie.items() if key in keys}
    info['genres'] = [genre['name'] for genre in movie['genres']]
    info['production_countries'] = [country['iso_3166_1'] for country in movie['production_countries']]
    info.update(get_credits(movie))

    # Debugging
    print("----PRINTING MOVIE INFO---")
    pprint(info)
    print('--------------------------')

    return info


def get_credits(movie):
    """
    Extracts credit information (e.g. Directors, actors, writers)
    :param movie: movie response JSON object from TMDb API v3
    :return: credits dictionary
    """
    credits = movie['credits']
    cast = credits['cast']
    crew = credits['crew']

    # Get top five actors and/or actresses
    actors = [person['name'].rstrip() for person in cast[:5]]
    # Get director(s)
    directors = [person['name'].rstrip() for person in crew if person['job'] == 'Director']
    # Get writer(s)
    writers = [person['name'].rstrip() for person in crew if person['job'] in ('Writer', 'Screenplay')]

    return {'actors': actors, 'directors': directors, 'writers': writers}





from textwrap import dedent
from utils.string_utils import formatted_date_str, formatted_num_str

def reply_to_user(info):
    """
    Replies to a user query on Twitter
    :param screen_name: user Twitter handle
    :param in_reply_to_status_id: query status ID
    :param info: movie info dictionary
    :return: None
    """
    screen_name = "mantis_chad69"
    reply_status = f"""
    @{screen_name}
    🎥 {info['original_title']}
    🗓️ Released {formatted_date_str(info['release_date'])}
    🕐 {info['runtime']} min
    ⭐ {info['vote_average']} rating
    💰 ${formatted_num_str(info['budget'])} budget
    💵 ${formatted_num_str(info['revenue'])} box office
    🎦 {', '.join(info['genres'])}
    🌐 {', '.join(info['production_countries'])}
    🎬 Directed by {', '.join(info['directors'])}
    👪 Starring {', '.join(info['actors'])}
    ✍ Written by {', '.join(info['writers'])}
    📑 Overview: {info['overview']}"""

    reply_status = dedent(reply_status)
    print(repr(reply_status))

    # api = create_api()
    # api.update_status(reply_status)

    #print(repr(dedent(reply_status)))
    #print(f"Length of reply: {len(reply_status)} chars")
    #print(reply_status.split('\n'))

    partition_status(reply_status)





def partition_status(status):
    """
    Splits a status string into statuses of 280 characters or less
    (i.e. the limit imposed on tweet lengths by Twitter)
    :param status: string
    :return: list of strings
    """
    print("--- PARTITIONING STATUS ---")
    # status = dedent(status)
    lines = status.split('\n')

    print("**SPLIT**")
    for line in lines:
        print(repr(line))

    # List of status strings to be tweeted
    statuses = []

    # Divide the original string into sub-tweets
    status = ''
    for index, line in enumerate(lines):
        # print(f"Line: {repr(line)}")
        # print(f"Status: {repr(status)}")
        if len(status + line) > 280:
            statuses.append(status)
            status = line
        else:
            status += line
            if index == len(lines) - 1:
                statuses.append(status)

    pprint("**STATUSES**")
    for status in statuses:
        print(f"Length: {len(status)}")
        print(repr(status))
    return statuses





def reply_to_self():
    api = create_api()
    status = api.update_status('Hello joe')

    reply_id = status.id
    screen_name = status.user.screen_name
    api.update_status(f'@{screen_name} Hello, just replying to myself!', in_reply_to_status_id=reply_id)


def upload_photo():
    api = create_api()
    try:
        filename = 'images/vScen3pRHnbtlfNxErROpiM8ABm.jpg'
        # filename = 'images/neds_dad.jpg'
        with open(filename) as image:
            media = api.update_with_media(filename, status="shut up idiot")
            # printing the information
            # print("The media ID is : " + media.media_id_string)
            # print("The size of the file is : " + str(media.size) + " bytes")
    except TweepError:
        print("Error uploading image")



from tweepy import TweepError


def main():
    # Authenticate to Twitter and create API object
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ['help', 'support'], since_id)
        logger.info('Waiting...')
        time.sleep(60)


if __name__ == "__main__":
    main()
    # api = create_api()
    # status = api.update_status("🎬 🕐 ⭐️💰 💵 🎥 🗓️ 🎦 (genre) ✍ 👪")
    # upload_photo()
