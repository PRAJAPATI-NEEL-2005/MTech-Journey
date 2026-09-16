from abc import ABC, abstractmethod
from typing import List, Optional
from business.models import Book

class BookRepository(ABC):
    @abstractmethod
    def add_book(self, book: Book) -> Book:
        pass

    @abstractmethod
    def get_all_books(self) -> List[Book]:
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        pass

    @abstractmethod
    def update_book(self, book: Book) -> None:
        pass

    @abstractmethod
    def delete_book(self, book_id: int) -> None:
        pass

    @abstractmethod
    def search_books(self, query: str) -> List[Book]:
        pass
