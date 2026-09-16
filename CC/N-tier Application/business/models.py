from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    id: Optional[int]
    title: str
    author: str
    isbn: str
    publication_year: int
    quantity: int
