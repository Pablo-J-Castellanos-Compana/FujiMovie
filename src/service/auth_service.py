import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def __init__(self, users_file='data/users.json'):
        self.users_file = users_file
        self.users = {}
        self._ensure_data_dir()
        self._load_users()
    
    def _ensure_data_dir(self):
        """Crea el directorio data si no existe"""
        os.makedirs(os.path.dirname(self.users_file) or '.', exist_ok=True)
    
    def _load_users(self):
        """Carga los usuarios del archivo JSON"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        else:
            self.users = {}
    
    def _save_users(self):
        """Guarda los usuarios en el archivo JSON"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=2, ensure_ascii=False)
    
    def register(self, username, email, password):
        """Registra un nuevo usuario"""
        # Validar que no existan duplicados
        for user_data in self.users.values():
            if user_data['username'] == username:
                return False, "El usuario ya existe"
            if user_data['email'] == email:
                return False, "El email ya está registrado"
        
        # Validar campos
        if not username or len(username) < 3:
            return False, "El usuario debe tener al menos 3 caracteres"
        if not email or '@' not in email:
            return False, "Email inválido"
        if not password or len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        # Crear nuevo usuario
        user_id = str(len(self.users) + 1)
        self.users[user_id] = {
            'id': user_id,
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'created_at': datetime.now().isoformat(),
            'library': []
        }
        self._save_users()
        return True, "Usuario registrado exitosamente"
    
    def login(self, username, password):
        """Autentica un usuario"""
        for user_id, user_data in self.users.items():
            if user_data['username'] == username:
                if check_password_hash(user_data['password_hash'], password):
                    return True, user_id
                else:
                    return False, "Contraseña incorrecta"
        return False, "Usuario no encontrado"
    
    def get_user(self, user_id):
        """Obtiene los datos de un usuario"""
        return self.users.get(user_id)
    
    def add_to_library(self, user_id, movie_id):
        """Añade una película a la biblioteca del usuario"""
        if user_id not in self.users:
            return False
        
        user_data = self.users[user_id]
        library = user_data.get('library', [])
        
        # Verificar si ya existe
        for item in library:
            if item['movie_id'] == movie_id:
                return True  # Ya está en la biblioteca
        
        # Añadir nueva película
        library.append({
            'movie_id': movie_id,
            'rating': None,
            'added_at': datetime.now().isoformat()
        })
        
        user_data['library'] = library
        self._save_users()
        return True
    
    def remove_from_library(self, user_id, movie_id):
        """Elimina una película de la biblioteca del usuario"""
        if user_id not in self.users:
            return False
        
        user_data = self.users[user_id]
        library = user_data.get('library', [])
        user_data['library'] = [item for item in library if item['movie_id'] != movie_id]
        self._save_users()
        return True
    
    def rate_movie(self, user_id, movie_id, rating):
        """Valora una película en la biblioteca"""
        if user_id not in self.users:
            return False
        
        user_data = self.users[user_id]
        library = user_data.get('library', [])
        
        for item in library:
            if item['movie_id'] == movie_id:
                item['rating'] = rating
                self._save_users()
                return True
        
        return False
    
    def is_in_library(self, user_id, movie_id):
        """Verifica si una película está en la biblioteca del usuario"""
        if user_id not in self.users:
            return False
        
        user_data = self.users[user_id]
        library = user_data.get('library', [])
        return any(item['movie_id'] == movie_id for item in library)
    
    def get_rating(self, user_id, movie_id):
        """Obtiene la valoración de una película"""
        if user_id not in self.users:
            return None
        
        user_data = self.users[user_id]
        library = user_data.get('library', [])
        
        for item in library:
            if item['movie_id'] == movie_id:
                return item.get('rating')
        
        return None
