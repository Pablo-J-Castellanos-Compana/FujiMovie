import requests
from model.movie import Movie
from model.user_movie import UserMovie
from typing import List, Optional
import urllib3
import json
import os

# Desactivar advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MovieService:
    def __init__(self):
        self.api_url = 'https://devsapihub.com/api-movies'
        self.timeout = 10
        self.library_file = os.path.join(os.path.dirname(__file__), '..', '..', 'library.json')
        self._ensure_library_file()

    def get_all_movies(self) -> List[Movie]:
        """Obtiene todas las películas"""
        try:
            response = requests.get(self.api_url, timeout=self.timeout, verify=False)
            response.raise_for_status()
            data = response.json()
            return [Movie(**movie) for movie in (data if isinstance(data, list) else [])]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        """Obtiene una película por ID"""
        try:
            response = requests.get(f"{self.api_url}/{movie_id}", timeout=self.timeout, verify=False)
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
            response = requests.get(f"{self.api_url}/genre/{genre}", timeout=self.timeout, verify=False)
            response.raise_for_status()
            data = response.json()
            return [Movie(**movie) for movie in (data if isinstance(data, list) else [])]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_movies_by_year(self, year: int) -> List[Movie]:
        """Obtiene películas por año"""
        try:
            response = requests.get(f"{self.api_url}/year/{year}", timeout=self.timeout, verify=False)
            response.raise_for_status()
            data = response.json()
            return [Movie(**movie) for movie in (data if isinstance(data, list) else [])]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_movies_by_stars(self, stars: float) -> List[Movie]:
        """Obtiene películas por calificación"""
        try:
            response = requests.get(f"{self.api_url}/stars/{stars}", timeout=self.timeout, verify=False)
            response.raise_for_status()
            data = response.json()
            return [Movie(**movie) for movie in (data if isinstance(data, list) else [])]
        except Exception as e:
            print(f"Error: {e}")
            return []

    def _ensure_library_file(self):
        """Asegura que el archivo de biblioteca existe"""
        if not os.path.exists(self.library_file):
            with open(self.library_file, 'w') as f:
                json.dump([], f)

    def _load_library(self) -> List[dict]:
        """Carga la biblioteca desde el archivo JSON"""
        try:
            with open(self.library_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def _save_library(self, library: List[dict]):
        """Guarda la biblioteca en el archivo JSON"""
        with open(self.library_file, 'w') as f:
            json.dump(library, f, indent=2)

    def add_to_library(self, movie_id: int, status: str = 'por ver') -> bool:
        """Añade una película a la biblioteca"""
        movie = self.get_movie_by_id(movie_id)
        if not movie:
            return False
        
        library = self._load_library()
        if any(item['movie_id'] == movie_id for item in library):
            return False  # Ya está en la biblioteca
        
        user_movie = {
            'movie_id': movie.id,
            'status': status,
            'title': movie.title,
            'description': movie.description,
            'year': movie.year,
            'image_url': movie.image_url,
            'genre': movie.genre,
            'stars': movie.stars
        }
        library.append(user_movie)
        self._save_library(library)
        return True

    def get_library(self) -> List[UserMovie]:
        """Obtiene la biblioteca del usuario"""
        library = self._load_library()
        return [UserMovie(**item) for item in library]

    def update_movie_status(self, movie_id: int, status: str) -> bool:
        """Actualiza el estado de una película en la biblioteca"""
        library = self._load_library()
        for item in library:
            if item['movie_id'] == movie_id:
                item['status'] = status
                self._save_library(library)
                return True
        return False

    def remove_from_library(self, movie_id: int) -> bool:
        """Elimina una película de la biblioteca"""
        library = self._load_library()
        new_library = [item for item in library if item['movie_id'] != movie_id]
        if len(new_library) < len(library):
            self._save_library(new_library)
            return True
        return False
