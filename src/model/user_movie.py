from dataclasses import dataclass
from typing import Optional

@dataclass
class UserMovie:
    movie_id: int
    status: str  # 'por ver' or 'visto'
    title: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    image_url: Optional[str] = None
    genre: Optional[str] = None
    stars: Optional[float] = None