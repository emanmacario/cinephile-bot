import os
import requests
from dotenv import load_dotenv, find_dotenv
from pprint import pprint

# This program uses the TMDb API but is not endorsed or certified by TMDb

# Load TMDb API key from .env
load_dotenv(find_dotenv())


class TMDb(object):
    # Static constants
    API_KEY = os.environ.get('API_KEY')
    API_VERSION = 3
    BASE_URI = f'https://api.themoviedb.org/{API_VERSION}'

    def get_endpoint_url(self, path):
        """
        Returns a URL for a TMDb API v3 endpoint
        :return: URL
        """
        return f'{self.BASE_URI}{path}'

    def _get_params(self, params=None):
        """
        Updates params dict with TMDb API key
        :param params: params dict
        :return: updated dict
        """
        api_key = {'api_key': self.API_KEY}
        if params:
            params.update(api_key)
        else:
            params = api_key
        return params

    def _GET(self, path, params=None):
        """
        :param path: TMDb API v3 endpoint path
        :param params: query string parameters
        :return: response JSON object
        """
        url = self.get_endpoint_url(path)
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Connection': 'close'}
        params = self._get_params(params)
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'

        return response.json()

    def search_movies(self, query):
        """
        Searches for possible movies that match a user's query
        :param query: string
        :return: search results JSON object
        """
        print(f"Searching for movie '{query}'")
        path = '/search/movie'
        params = {'query': query}

        return self._GET(path, params)

    def get_movie_by_id(self, movie_id):
        """
        Retrieves a movie from TMDb with a specific ID
        :param movie_id: movie ID
        :return: response JSON object
        """
        print(f"Retrieving movie with ID: {movie_id}")
        path = f'/movie/{movie_id}'
        params = {'append_to_response': 'credits'}

        return self._GET(path, params)

    def _get_configuration(self):
        """
        Gets configuration details for TMDb API v3
        :return: configuration details
        """
        print(f"Retrieving TMDb API v3 configuration details")
        path = '/configuration'

        return self._GET(path, None)

    def get_image_url(self, path):
        """
        Gets full image URL for a given path
        :param path: image path
        :return: image URL
        """
        configuration = self._get_configuration()
        secure_base_url = configuration['images']['secure_base_url']
        file_size = 'original'

        return f'{secure_base_url}{file_size}{path}'


def main():
    tmdb = TMDb()
    response = tmdb._get_configuration()
    pprint(response)

    secure_base_url = 'https://image.tmdb.org/t/p/'
    file_size = 'original'
    image_path = '/vScen3pRHnbtlfNxErROpiM8ABm.jpg'

    print(f"URL: {secure_base_url}{file_size}{image_path}")


if __name__ == "__main__":
    main()
