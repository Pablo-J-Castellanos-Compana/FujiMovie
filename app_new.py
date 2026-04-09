import sys
import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from service.movie_service import MovieService
from controller.movie_controller import movie_bp

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='src/templates')
movie_service = MovieService()

# Register blueprints
app.register_blueprint(movie_bp)

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
    return render_template('movies/details.html', movie=movie)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, message="Página no encontrada"), 404

if __name__ == '__main__':
    print("🎬 Iniciando FujiMovie...")
    print("📍 URL: http://localhost:5000")
    print("API: https://devsapihub.com/api-movies")
    app.run(debug=True, port=5000)
