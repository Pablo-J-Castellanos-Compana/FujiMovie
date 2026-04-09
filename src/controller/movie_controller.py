from flask import Blueprint, request, jsonify
from service.movie_service import MovieService

movie_bp = Blueprint('movies', __name__, url_prefix='/api/movies')
movie_service = MovieService()

@movie_bp.route('/search', methods=['GET'])
def search_movie():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Title parameter is required'}), 400

    try:
        movie = movie_service.search_movie(title)
        return jsonify({
            'title': movie.title,
            'year': movie.year,
            'genre': movie.genre,
            'director': movie.director,
            'runtime': movie.runtime,
            'plot': movie.plot,
            'poster': movie.poster
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500