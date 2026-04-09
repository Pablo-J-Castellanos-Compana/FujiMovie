from flask import Blueprint, request, jsonify
from service.movie_service import MovieService

movie_bp = Blueprint('movies', __name__, url_prefix='/api/movies')
movie_service = MovieService()

@movie_bp.route('', methods=['GET'])
def get_all_movies():
    """Obtiene todas las películas"""
    movies = movie_service.get_all_movies()
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'description': m.description,
        'year': m.year,
        'imageUrl': m.imageUrl,
        'genre': m.genre,
        'stars': m.stars
    } for m in movies])

@movie_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Obtiene una película por ID"""
    movie = movie_service.get_movie_by_id(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'year': movie.year,
        'imageUrl': movie.imageUrl,
        'genre': movie.genre,
        'stars': movie.stars
    })

@movie_bp.route('/search', methods=['GET'])
def search_movies():
    """Busca películas"""
    query = request.args.get('q', '').strip()
    genre = request.args.get('genre', '').strip()
    year = request.args.get('year', '').strip()
    stars = request.args.get('stars', '').strip()
    
    if query:
        movies = movie_service.search_movies(query)
    elif genre:
        movies = movie_service.get_movies_by_genre(genre)
    elif year:
        movies = movie_service.get_movies_by_year(int(year))
    elif stars:
        movies = movie_service.get_movies_by_stars(float(stars))
    else:
        movies = movie_service.get_all_movies()
    
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'description': m.description,
        'year': m.year,
        'imageUrl': m.imageUrl,
        'genre': m.genre,
        'stars': m.stars
    } for m in movies])