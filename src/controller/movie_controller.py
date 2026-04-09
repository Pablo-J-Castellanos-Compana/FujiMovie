from flask import Blueprint, request, jsonify
from service.movie_service import MovieService
from model.user_movie import UserMovie

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
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'description': m.description,
        'year': m.year,
        'imageUrl': m.imageUrl,
        'genre': m.genre,
        'stars': m.stars
    } for m in movies])

@movie_bp.route('/library', methods=['GET'])
def get_library():
    """Obtiene la biblioteca del usuario"""
    user_movies = movie_service.get_library()
    return jsonify([{
        'movie_id': um.movie_id,
        'status': um.status,
        'title': um.title,
        'description': um.description,
        'year': um.year,
        'image_url': um.image_url,
        'genre': um.genre,
        'stars': um.stars
    } for um in user_movies])

@movie_bp.route('/library', methods=['POST'])
def add_to_library():
    """Añade una película a la biblioteca"""
    data = request.get_json()
    movie_id = data.get('movie_id')
    status = data.get('status', 'por ver')
    if not movie_id:
        return jsonify({'error': 'movie_id is required'}), 400
    success = movie_service.add_to_library(movie_id, status)
    if success:
        return jsonify({'message': 'Movie added to library'}), 201
    else:
        return jsonify({'error': 'Movie not found or already in library'}), 400

@movie_bp.route('/library/<int:movie_id>', methods=['PUT'])
def update_movie_status(movie_id):
    """Actualiza el estado de una película en la biblioteca"""
    data = request.get_json()
    status = data.get('status')
    if not status or status not in ['por ver', 'visto']:
        return jsonify({'error': 'Invalid status'}), 400
    success = movie_service.update_movie_status(movie_id, status)
    if success:
        return jsonify({'message': 'Status updated'}), 200
    else:
        return jsonify({'error': 'Movie not in library'}), 404

@movie_bp.route('/library/<int:movie_id>', methods=['DELETE'])
def remove_from_library(movie_id):
    """Elimina una película de la biblioteca"""
    success = movie_service.remove_from_library(movie_id)
    if success:
        return jsonify({'message': 'Movie removed from library'}), 200
    else:
        return jsonify({'error': 'Movie not in library'}), 404