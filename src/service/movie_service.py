import requests
from model.movie import Movie
from typing import List, Optional

class MovieService:
    def __init__(self):
        self.api_url = 'https://devsapihub.com/api-movies'
        self.timeout = 10

    def get_all_movies(self) -> List[Movie]:
        """Obtiene todas las películas"""
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return [Movie(**movie) for movie in (data if isinstance(data, list) else [])]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        """Obtiene una película por ID"""
        try:
            response = requests.get(f"{self.api_url}/{movie_id}", timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and data:
                return Movie(**data[0])
            elif isinstance(data, dict):
                return Movie(**data)
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_movies_by_genre(self, genre: str) -> List[Movie]:
        """Obtiene películas por género"""
        try:
            response = requests.get(f"{self.api_url}/genre/{genre}", timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return [Movie(**movie) for movie in (data if isinstance(data, list) else [])]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_movies_by_year(self, year: int) -> List[Movie]:
        """Obtiene películas por año"""
        try:
            response = requests.get(f"{self.api_url}/year/{year}", timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return [Movie(**movie) for movie in (data if isinstance(data, list) else [])]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_movies_by_stars(self, stars: float) -> List[Movie]:
        """Obtiene películas por calificación"""
        try:
            response = requests.get(f"{self.api_url}/stars/{stars}", timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return [Movie(**movie) for movie in (data if isinstance(data, list) else [])]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def search_movies(self, query: str) -> List[Movie]:
        """Busca películas por título o descripción"""
        all_movies = self.get_all_movies()
        query_lower = query.lower()
        return [
            movie for movie in all_movies
            if query_lower in movie.title.lower() or query_lower in movie.description.lower()
        ]