import datetime
from typing import List
from business.models import Book
from business.exceptions import ValidationError, BookNotFoundError, OutOfStockError
from data.book_repository import BookRepository

class BookManager:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def add_book(self, title: str, author: str, isbn: str, publication_year: int, quantity: int) -> Book:
        self._validate_book_data(title, author, isbn, publication_year, quantity)
        book = Book(None, title, author, isbn, publication_year, quantity)
        return self.repository.add_book(book)

    def view_all_books(self) -> List[Book]:
        return self.repository.get_all_books()

    def search_books(self, query: str) -> List[Book]:
        if not query.strip():
            return []
        return self.repository.search_books(query)

    def get_book(self, book_id: int) -> Book:
        book = self.repository.get_book_by_id(book_id)
        if not book:
            raise BookNotFoundError(f"Book with ID {book_id} not found.")
        return book

    def update_book(self, book_id: int, title: str, author: str, isbn: str, publication_year: int, quantity: int) -> None:
        self._validate_book_data(title, author, isbn, publication_year, quantity)
        book = self.get_book(book_id)
        
        book.title = title
        book.author = author
        book.isbn = isbn
        book.publication_year = publication_year
        book.quantity = quantity
        
        self.repository.update_book(book)

    def delete_book(self, book_id: int) -> None:
        # Check if exists
        self.get_book(book_id)
        self.repository.delete_book(book_id)

    def check_out_book(self, book_id: int) -> None:
        book = self.get_book(book_id)
        if book.quantity <= 0:
            raise OutOfStockError(f"Book '{book.title}' is out of stock and cannot be checked out.")
        
        book.quantity -= 1
        self.repository.update_book(book)

    def _validate_book_data(self, title: str, author: str, isbn: str, publication_year: int, quantity: int):
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty.")
        if not author or not author.strip():
            raise ValidationError("Author cannot be empty.")
        
        current_year = datetime.datetime.now().year
        if publication_year > current_year:
            raise ValidationError(f"Publication year cannot be in the future (max {current_year}).")
            
        isbn_stripped = isbn.strip().replace('-', '')
        if len(isbn_stripped) not in [10, 13] or not isbn_stripped.isdigit():
            raise ValidationError("ISBN must be exactly 10 or 13 digits.")
            
        if quantity < 0:
            raise ValidationError("Quantity cannot be negative.")
