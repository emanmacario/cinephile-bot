import logging
import os
import time
import tweepy
from pprint import pformat
from textwrap import dedent
from tmdb.search import TMDb
from tweepy import TweepError
from twitter.auth import create_api
from utils.file_utils import save_image_from_url, delete_image
from utils.string_utils import formatted_date_str, formatted_num_str

# Set logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, tmdb, since_id):
    """
    Checks the bot's mentions timeline for
    new user queries, and replies to them
    :param api: Tweepy API object
    :param tmdb: TMDb API object
    :param since_id: latest tweet ID
    :return: None
    """
    logger.info('Retrieving mentions')
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        hashtags = tweet.entities['hashtags']
        new_query = False
        for hashtag in hashtags:
            if hashtag['text'] == 'movie':
                index = hashtag['indices'][1] + 1
                logger.info(f"Received query for movie '{tweet.text[index:]}' from @{tweet.user.screen_name}")
                movie_name = tweet.text[index:]
                new_query = True
                break

        new_since_id = max(tweet.id, new_since_id)

        # Tweet is ignored if it is a reply to another tweet
        if tweet.in_reply_to_status_id is not None:
            continue

        if new_query:
            movies = tmdb.search_movies(movie_name)
            if movies['total_results'] > 0:
                top_result = movies['results'][0]
                movie_id = top_result['id']
                movie = tmdb.get_movie_by_id(movie_id)
                info = extract_info(tmdb, movie)
            else:
                info = None
            reply_to_user(api, tweet, info)

    return new_since_id


def extract_info(tmdb, movie):
    """
    Extracts key information from primary information given in the JSON response object
    :param tmdb: TMDb API object
    :param movie: response JSON object
    :return: dictionary
    """
    # Keys for required information
    keys = ('original_title',
            'release_date',
            'runtime',
            'vote_average',
            'budget',
            'revenue',
            'overview',
            'poster_path',
            'backdrop_path')

    # Extract relevant information from response object
    info = {key: value for key, value in movie.items() if key in keys}
    info['genres'] = [genre['name'] for genre in movie['genres']]
    info['production_countries'] = [country['name'] for country in movie['production_countries']]
    info['poster_url'] = tmdb.get_image_url(info['poster_path'])
    info['backdrop_url'] = tmdb.get_image_url(info['backdrop_path'])
    info.update(get_credits(movie))

    # Save the film poster image locally
    save_image_from_url(info['poster_path'], info['poster_url'])

    # Logging
    logger.info("Movie Information")
    logger.info(pformat(info))

    return info


def get_credits(movie):
    """
    Extracts credit information (e.g. Directors, actors, writers)
    :param movie: movie response JSON object from TMDb API v3
    :return: credits dictionary
    """
    cast = movie['credits']['cast']
    crew = movie['credits']['crew']

    # Get top five actors and/or actresses
    actors = [person['name'] for person in cast[:5]]
    # Get director(s)
    directors = [person['name'] for person in crew if person['job'] == 'Director']
    # Get writer(s)
    writers = [person['name'] for person in crew if person['job'] in ('Writer', 'Screenplay')]

    return {'actors': actors, 'directors': directors, 'writers': writers}


def reply_to_user(api, tweet, info):
    """
    Replies to a user query on Twitter
    :param api: Tweepy API object
    :param tweet: tweet object to reply to
    :param info: movie information dictionary
    :return: None
    """
    # Generate a reply status for the query tweet
    reply_screen_name = tweet.user.screen_name
    if info is not None:
        reply_status = f"""
        @{reply_screen_name}
        🎥 {info['original_title']}
        🗓️ Released {formatted_date_str(info['release_date'])}
        🕐 {info['runtime']} min
        ⭐ {info['vote_average']} rating
        💰 ${formatted_num_str(info['budget'])} budget
        💵 ${formatted_num_str(info['revenue'])} box office
        🎦 {', '.join(info['genres'])}
        🌐 {', '.join(info['production_countries'])}
        🎬 Directed by {', '.join(info['directors'])}
        ✍ Written by {', '.join(info['writers'])}
        👪 Starring {', '.join(info['actors'])}
        📑 Overview: {info['overview']}"""
        reply_status = dedent(reply_status)
    else:
        reply_status = f"@{reply_screen_name} Sorry, I could not find that movie!"

    # Split the tweet into smaller sub-tweets if necessary
    user_screen_name = api.me().screen_name
    statuses = partition_status(user_screen_name, reply_status)

    # Reply to the user, backing off in linearly increasing
    # intervals if we have exceeded Twitter API's rate limits
    backoffs = 1
    while True:
        try:
            for index, status in enumerate(statuses):
                logger.info(f"Tweeting: '{status}'")
                if info is None:
                    tweet = api.update_status(status, in_reply_to_status_id=tweet.id)
                    continue

                image_filename = f"images{info['poster_path']}"
                if not index and os.path.exists(image_filename):
                    tweet = api.update_with_media(image_filename, status=status, in_reply_to_status_id=tweet.id)
                    delete_image(info['poster_path'])
                else:
                    tweet = api.update_status(status, in_reply_to_status_id=tweet.id)
            break
        except TweepError as e:
            logger.error(e.reason)
            time.sleep(backoffs * 10)
            backoffs += 1
            continue


def partition_status(screen_name, status):
    """
    Splits a status string into statuses of 280 characters or less
    (i.e. the limit imposed on tweet lengths by Twitter)
    :param screen_name: authenticated Twitter user's screen name
    :param status: string
    :return: list of strings
    """
    # status = dedent(status)
    lines = status.split('\n')

    # List of status strings to be tweeted
    statuses = []

    # Divide the original tweet string into smaller tweets
    status = ''
    for index, line in enumerate(lines):
        # print(f"Line: {repr(line)}")
        # print(f"Status: {repr(status)}")
        line = f'{line}\n'

        # Since each emoji is two characters and we use 12 emojis (i.e. 280-12=268)
        TOTAL_EMOJIS = 12
        if len(status + line) > 280 - TOTAL_EMOJIS:
            statuses.append(status)
            status = f'@{screen_name} {line}'
        else:
            status += line
            if index == len(lines) - 1:
                statuses.append(status)

    return statuses


def max_since_id(api):
    """
    Returns the maximum since ID such that no
    tweets with lesser since IDs are replied to
    :param api: Tweepy API object
    :return: max since ID
    """
    return max(tweet.id for tweet in tweepy.Cursor(api.mentions_timeline).items())


def main():
    # Authenticate to Twitter and create API objects
    api = create_api()
    tmdb = TMDb()
    since_id = max_since_id(api)

    # Main loop of bot
    while True:
        since_id = check_mentions(api, tmdb, since_id)
        logger.info('Main thread sleeping...')
        time.sleep(10)


if __name__ == "__main__":
    main()