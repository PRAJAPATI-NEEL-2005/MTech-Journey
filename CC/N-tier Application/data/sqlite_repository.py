import sqlite3
from typing import List, Optional
from business.models import Book
from data.book_repository import BookRepository

class SQLiteRepository(BookRepository):
    def __init__(self, db_path: str = "library.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT NOT NULL,
                    publication_year INTEGER NOT NULL,
                    quantity INTEGER NOT NULL
                )
            ''')
            conn.commit()
        finally:
            conn.close()

    def _row_to_book(self, row: sqlite3.Row) -> Book:
        return Book(
            id=row['id'],
            title=row['title'],
            author=row['author'],
            isbn=row['isbn'],
            publication_year=row['publication_year'],
            quantity=row['quantity']
        )

    def add_book(self, book: Book) -> Book:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (title, author, isbn, publication_year, quantity)
                VALUES (?, ?, ?, ?, ?)
            ''', (book.title, book.author, book.isbn, book.publication_year, book.quantity))
            book.id = cursor.lastrowid
            conn.commit()
            return book
        finally:
            conn.close()

    def get_all_books(self) -> List[Book]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books')
            return [self._row_to_book(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_book(row)
            return None
        finally:
            conn.close()

    def update_book(self, book: Book) -> None:
        if book.id is None:
            raise ValueError("Book ID cannot be None when updating")
        
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE books
                SET title = ?, author = ?, isbn = ?, publication_year = ?, quantity = ?
                WHERE id = ?
            ''', (book.title, book.author, book.isbn, book.publication_year, book.quantity, book.id))
            conn.commit()
        finally:
            conn.close()

    def delete_book(self, book_id: int) -> None:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM books WHERE id = ?', (book_id,))
            if cursor.fetchone() is None:
                return
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
        finally:
            conn.close()

    def search_books(self, query: str) -> List[Book]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            search_pattern = f"%{query}%"
            cursor.execute('''
                SELECT * FROM books
                WHERE title LIKE ? OR author LIKE ?
            ''', (search_pattern, search_pattern))
            return [self._row_to_book(row) for row in cursor.fetchall()]
        finally:
            conn.close()
