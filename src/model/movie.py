from dataclasses import dataclass

@dataclass
class Movie:
    title: str
    year: str
    genre: str
    director: str
    runtime: str
    plot: str
    poster: str