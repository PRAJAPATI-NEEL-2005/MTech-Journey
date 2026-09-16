import unittest
import datetime
from business.book_manager import BookManager
from business.exceptions import ValidationError, OutOfStockError, BookNotFoundError
from data.memory_repository import MemoryRepository

class TestBusinessLogic(unittest.TestCase):
    def setUp(self):
        # We use a mocked/in-memory data layer to test business logic in isolation
        self.repository = MemoryRepository()
        self.manager = BookManager(self.repository)

    def test_add_valid_book(self):
        book = self.manager.add_book("Test Title", "Author", "1234567890", 2023, 5)
        self.assertEqual(book.title, "Test Title")
        self.assertEqual(book.quantity, 5)
        self.assertEqual(len(self.repository.books), 1)

    def test_add_book_empty_title_or_author(self):
        with self.assertRaises(ValidationError):
            self.manager.add_book("", "Author", "1234567890", 2023, 5)
        with self.assertRaises(ValidationError):
            self.manager.add_book("Title", "   ", "1234567890", 2023, 5)

    def test_add_book_invalid_year(self):
        future_year = datetime.datetime.now().year + 1
        with self.assertRaises(ValidationError):
            self.manager.add_book("Title", "Author", "1234567890", future_year, 5)

    def test_add_book_invalid_isbn(self):
        # 9 digits (invalid)
        with self.assertRaises(ValidationError):
            self.manager.add_book("Title", "Author", "123456789", 2023, 5)
        # 11 digits (invalid)
        with self.assertRaises(ValidationError):
            self.manager.add_book("Title", "Author", "12345678901", 2023, 5)
        # contains letters
        with self.assertRaises(ValidationError):
            self.manager.add_book("Title", "Author", "123456789X", 2023, 5)
            
        # 13 digits (valid)
        book = self.manager.add_book("Title", "Author", "1234567890123", 2023, 5)
        self.assertIsNotNone(book.id)

    def test_add_book_negative_quantity(self):
        with self.assertRaises(ValidationError):
            self.manager.add_book("Title", "Author", "1234567890", 2023, -1)

    def test_checkout_book_decreases_quantity(self):
        book = self.manager.add_book("Title", "Author", "1234567890", 2023, 1)
        self.manager.check_out_book(book.id)
        
        updated_book = self.manager.get_book(book.id)
        self.assertEqual(updated_book.quantity, 0)

    def test_checkout_out_of_stock_book(self):
        book = self.manager.add_book("Title", "Author", "1234567890", 2023, 0)
        with self.assertRaises(OutOfStockError):
            self.manager.check_out_book(book.id)

    def test_update_book_validations(self):
        book = self.manager.add_book("Title", "Author", "1234567890", 2023, 5)
        
        # Updating with empty title should fail validation
        with self.assertRaises(ValidationError):
            self.manager.update_book(book.id, "", "Author", "1234567890", 2023, 5)
            
        # Updating with valid data
        self.manager.update_book(book.id, "New Title", "Author", "1234567890", 2023, 5)
        updated_book = self.manager.get_book(book.id)
        self.assertEqual(updated_book.title, "New Title")

    def test_get_nonexistent_book(self):
        with self.assertRaises(BookNotFoundError):
            self.manager.get_book(999)

if __name__ == '__main__':
    unittest.main()
