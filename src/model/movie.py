from dataclasses import dataclass

@dataclass
class Movie:
    id: int
    title: str
    description: str
    year: int
    image_url: str
    genre: str
    stars: float