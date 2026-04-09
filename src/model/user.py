from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now()
        self.library = []  # Lista de películas en la biblioteca
    
    def set_password(self, password):
        """Hash y almacena la contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña es correcta"""
        return check_password_hash(self.password_hash, password)
    
    def add_to_library(self, movie_id, rating=None):
        """Añade una película a la biblioteca"""
        # Verificar si ya existe
        for item in self.library:
            if item['movie_id'] == movie_id:
                if rating is not None:
                    item['rating'] = rating
                item['added_at'] = datetime.now()
                return
        
        # Añadir nueva película
        self.library.append({
            'movie_id': movie_id,
            'rating': rating,
            'added_at': datetime.now()
        })
    
    def remove_from_library(self, movie_id):
        """Elimina una película de la biblioteca"""
        self.library = [item for item in self.library if item['movie_id'] != movie_id]
    
    def rate_movie(self, movie_id, rating):
        """Valora una película en la biblioteca"""
        for item in self.library:
            if item['movie_id'] == movie_id:
                item['rating'] = rating
                return True
        return False
    
    def is_in_library(self, movie_id):
        """Verifica si una película está en la biblioteca"""
        return any(item['movie_id'] == movie_id for item in self.library)
    
    def get_rating(self, movie_id):
        """Obtiene la valoración de una película"""
        for item in self.library:
            if item['movie_id'] == movie_id:
                return item.get('rating')
        return None
