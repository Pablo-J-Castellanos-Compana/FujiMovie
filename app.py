import sys
import os
from flask import Flask
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from controller.movie_controller import movie_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Register blueprints
app.register_blueprint(movie_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8080)