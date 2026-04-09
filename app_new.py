import sys
import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from functools import wraps

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from service.movie_service import MovieService
from service.auth_service import AuthService
from controller.movie_controller import movie_bp

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='src/templates')
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
movie_service = MovieService()
auth_service = AuthService()

# Register blueprints
app.register_blueprint(movie_bp)

# Decorador para proteger rutas que requieren autenticación
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('list_movies'))

@app.route('/movies')
def list_movies():
    search = request.args.get('search', '').strip()
    genre = request.args.get('genre', '').strip()
    year = request.args.get('year', '').strip()
    stars = request.args.get('stars', '').strip()
    
    movies = []
    filter_type = None
    filter_value = None
    
    try:
        if search:
            movies = movie_service.search_movies(search)
            filter_type = "Búsqueda"
            filter_value = search
        elif genre:
            movies = movie_service.get_movies_by_genre(genre)
            filter_type = "Género"
            filter_value = genre
        elif year:
            movies = movie_service.get_movies_by_year(int(year))
            filter_type = "Año"
            filter_value = year
        elif stars:
            movies = movie_service.get_movies_by_stars(float(stars))
            filter_type = "Estrellas"
            filter_value = stars
        else:
            movies = movie_service.get_all_movies()
    except Exception as e:
        print(f"Error: {e}")
    
    return render_template('movies/list.html', movies=movies, filter_type=filter_type, filter_value=filter_value, search_query=search if search else None)

@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movie = movie_service.get_movie_by_id(movie_id)
    if not movie:
        return redirect(url_for('list_movies'))
    
    is_in_library = False
    current_rating = None
    
    if 'user_id' in session:
        user_id = session.get('user_id')
        is_in_library = auth_service.is_in_library(user_id, movie_id)
        current_rating = auth_service.get_rating(user_id, movie_id)
    
    return render_template('movies/details.html', movie=movie, is_in_library=is_in_library, current_rating=current_rating)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if password != confirm_password:
            return render_template('auth/register.html', error="Las contraseñas no coinciden")
        
        success, message = auth_service.register(username, email, password)
        if success:
            return redirect(url_for('login', success='true'))
        else:
            return render_template('auth/register.html', error=message)
    
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        success, result = auth_service.login(username, password)
        if success:
            session['user_id'] = result
            user_data = auth_service.get_user(result)
            session['username'] = user_data['username']
            return redirect(url_for('list_movies'))
        else:
            return render_template('auth/login.html', error=result)
    
    success = request.args.get('success')
    return render_template('auth/login.html', success=success)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('list_movies'))

@app.route('/library')
@login_required
def library():
    user_id = session.get('user_id')
    user_data = auth_service.get_user(user_id)
    
    # Obtener datos completos de las películas en la biblioteca
    library_movies = []
    for item in user_data.get('library', []):
        movie = movie_service.get_movie_by_id(item['movie_id'])
        if movie:
            movie_dict = {
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'year': movie.year,
                'image_url': movie.image_url,
                'genre': movie.genre,
                'stars': movie.stars,
                'rating': item.get('rating'),
                'added_at': item.get('added_at')
            }
            library_movies.append(movie_dict)
    
    return render_template('library.html', library_movies=library_movies)

@app.route('/add_to_library/<int:movie_id>', methods=['POST'])
def add_to_library(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    auth_service.add_to_library(user_id, movie_id)
    return redirect(url_for('movie_details', movie_id=movie_id))

@app.route('/remove_from_library/<int:movie_id>', methods=['POST'])
def remove_from_library(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    auth_service.remove_from_library(user_id, movie_id)
    return redirect(request.referrer or url_for('library'))

@app.route('/rate_movie/<int:movie_id>', methods=['POST'])
def rate_movie(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    rating = request.form.get('rating', type=float)
    
    if rating and 0 <= rating <= 5:
        auth_service.rate_movie(user_id, movie_id, rating)
    
    return redirect(request.referrer or url_for('movie_details', movie_id=movie_id))

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, message="Página no encontrada"), 404

if __name__ == '__main__':
    print("🎬 Iniciando FujiMovie...")
    print("📍 URL: http://localhost:5000")
    print("API: https://devsapihub.com/api-movies")
    app.run(debug=True, port=5000)
