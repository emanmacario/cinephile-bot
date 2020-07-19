import json
import os
import requests
from dotenv import load_dotenv, find_dotenv
from pprint import pprint

# This program uses the TMDb API but is not endorsed or certified by TMDb

# Image docs link: https://developers.themoviedb.org/3/getting-started/images


load_dotenv(find_dotenv())
API_KEY = os.environ.get('API_KEY')
API_VERSION = 3
BASE_URI = f'https://api.themoviedb.org/{API_VERSION}'


def get_endpoint_url(path):
    return f'{BASE_URI}{path}'


def get_params(params):
    # TODO: Set API key here
    pass


def _GET(path, params=None):
    """
    :param path: TMDb API v3 endpoint path
    :param params: query string parameters
    :return: response JSON object
    """
    url = get_endpoint_url(path)
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Connection': 'close'}
    api_key = {'api_key': API_KEY}
    if params:
        params.update(api_key)
    else:
        params = api_key
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    response.encoding = 'utf-8'

    return response.json()


def search_for_movie(query):
    """
    Searches for possible movies that match a user's query
    :param query: string
    :return: top-k TMDb movie IDs (k=5)
    """
    print(f"Searching for movie '{query}'")
    path = '/search/movie'
    params = {'query': query}

    return _GET(path, params)


def get_movie(movie_id):
    """
    Retrieves a movie from TMDb with a specific ID
    :param movie_id: movie ID
    :return: response JSON obejct
    """
    print(f"Retrieving movie with ID: {movie_id}")
    path = f'/movie/{movie_id}'
    params = {'append_to_response': 'credits'}

    return _GET(path, params)


# TODO: Store this shit as class method on object initiation
def get_configuration():
    """
    Gets configuration details for TMDb API v3
    :return: configuration details
    """
    print(f"Retrieving TMDb API v3 configuration details")
    path = '/configuration'

    return _GET(path, None)


def get_image_url(path):
    """
    Gets full image URL for a given path
    :param path: image path
    :return: image URL
    """
    configuration = get_configuration()
    secure_base_url = configuration['images']['secure_base_url']
    file_size = 'original'

    return f'{secure_base_url}{file_size}{path}'


def main():
    # query = 'The Lighthouse'
    # print(API_KEY)
    #
    # result = search_for_movie(query)
    # print(type(result))
    # pprint(result)

    # movie_id = 299534  # Avengers endgame
    # result = get_movie(movie_id)
    # pprint(result)
    response = get_configuration()
    pprint(response)

    secure_base_url = 'https://image.tmdb.org/t/p/'
    file_size = 'original'
    image_path = '/vScen3pRHnbtlfNxErROpiM8ABm.jpg'

    print(f"URL: {secure_base_url}{file_size}{image_path}")


if __name__ == "__main__":
    main()
