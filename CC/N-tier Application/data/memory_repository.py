from typing import List, Optional
from business.models import Book
from data.book_repository import BookRepository

class MemoryRepository(BookRepository):
    def __init__(self):
        self.books: List[Book] = []
        self.next_id = 1

    def add_book(self, book: Book) -> Book:
        book.id = self.next_id
        self.next_id += 1
        self.books.append(book)
        return book

    def get_all_books(self) -> List[Book]:
        return list(self.books)

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def update_book(self, book: Book) -> None:
        for i, b in enumerate(self.books):
            if b.id == book.id:
                self.books[i] = book
                return
        raise ValueError(f"Book with id {book.id} not found")

    def delete_book(self, book_id: int) -> None:
        self.books = [b for b in self.books if b.id != book_id]

    def search_books(self, query: str) -> List[Book]:
        query = query.lower()
        return [
            b for b in self.books
            if query in b.title.lower() or query in b.author.lower()
        ]
