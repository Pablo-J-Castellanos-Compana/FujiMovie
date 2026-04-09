from dataclasses import dataclass

@dataclass
class Movie:
    id: int
    title: str
    description: str
    year: int
    imageUrl: str
    genre: str
    stars: float