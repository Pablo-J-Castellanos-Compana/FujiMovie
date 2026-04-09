import os
import requests
from model.movie import Movie

class MovieService:
    def __init__(self):
        self.api_key = os.getenv('OMDB_API_KEY')
        self.api_url = 'http://www.omdbapi.com/'

    def search_movie(self, title: str) -> Movie:
        params = {
            't': title,
            'apikey': self.api_key
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get('Response') == 'False':
            raise ValueError(f"Movie not found: {data.get('Error', 'Unknown error')}")

        return Movie(
            title=data.get('Title', ''),
            year=data.get('Year', ''),
            genre=data.get('Genre', ''),
            director=data.get('Director', ''),
            runtime=data.get('Runtime', ''),
            plot=data.get('Plot', ''),
            poster=data.get('Poster', '')
        )