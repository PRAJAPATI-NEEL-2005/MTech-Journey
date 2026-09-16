import sys
from business.book_manager import BookManager
from business.exceptions import BookException, ValidationError, OutOfStockError

class CLI:
    def __init__(self, book_manager: BookManager):
        self.manager = book_manager

    def print_menu(self):
        print("\n=== Library Management System ===")
        print("1. Add a book")
        print("2. View all books")
        print("3. Search books")
        print("4. Update a book")
        print("5. Delete a book")
        print("6. Check out a book")
        print("7. Exit")
        print("=================================")

    def run(self):
        while True:
            self.print_menu()
            choice = input("Enter choice (1-7): ")
            
            try:
                if choice == '1':
                    self._add_book()
                elif choice == '2':
                    self._view_all_books()
                elif choice == '3':
                    self._search_books()
                elif choice == '4':
                    self._update_book()
                elif choice == '5':
                    self._delete_book()
                elif choice == '6':
                    self._check_out_book()
                elif choice == '7':
                    print("Exiting application...")
                    sys.exit(0)
                else:
                    print("Invalid choice. Please enter a number from 1 to 7.")
            except BookException as e:
                print(f"\n[ERROR] {str(e)}")
            except Exception as e:
                print(f"\n[UNEXPECTED ERROR] {str(e)}")

    def _add_book(self):
        print("\n-- Add Book --")
        title = input("Title: ")
        author = input("Author: ")
        isbn = input("ISBN (10 or 13 digits): ")
        
        try:
            year = int(input("Publication Year: "))
            quantity = int(input("Quantity: "))
        except ValueError:
            raise ValidationError("Year and Quantity must be integers.")
            
        book = self.manager.add_book(title, author, isbn, year, quantity)
        print(f"\nSuccess! Book '{book.title}' added with ID: {book.id}")

    def _view_all_books(self):
        print("\n-- All Books --")
        books = self.manager.view_all_books()
        self._print_books(books)

    def _search_books(self):
        print("\n-- Search Books --")
        query = input("Enter title or author to search: ")
        books = self.manager.search_books(query)
        self._print_books(books)

    def _update_book(self):
        print("\n-- Update Book --")
        try:
            book_id = int(input("Enter Book ID to update: "))
        except ValueError:
            raise ValidationError("Book ID must be an integer.")
            
        # Ensure book exists before asking for details
        book = self.manager.get_book(book_id)
        print(f"Updating '{book.title}' (Leave blank to keep current value)")
        
        title = input(f"Title [{book.title}]: ") or book.title
        author = input(f"Author [{book.author}]: ") or book.author
        isbn = input(f"ISBN [{book.isbn}]: ") or book.isbn
        
        year_str = input(f"Publication Year [{book.publication_year}]: ")
        year = int(year_str) if year_str else book.publication_year
        
        qty_str = input(f"Quantity [{book.quantity}]: ")
        quantity = int(qty_str) if qty_str else book.quantity
        
        self.manager.update_book(book_id, title, author, isbn, year, quantity)
        print("\nSuccess! Book updated.")

    def _delete_book(self):
        print("\n-- Delete Book --")
        try:
            book_id = int(input("Enter Book ID to delete: "))
        except ValueError:
            raise ValidationError("Book ID must be an integer.")
            
        self.manager.delete_book(book_id)
        print("\nSuccess! Book deleted.")

    def _check_out_book(self):
        print("\n-- Check Out Book --")
        try:
            book_id = int(input("Enter Book ID to check out: "))
        except ValueError:
            raise ValidationError("Book ID must be an integer.")
            
        self.manager.check_out_book(book_id)
        print("\nSuccess! Book checked out (quantity decreased by 1).")

    def _print_books(self, books):
        if not books:
            print("No books found.")
            return
            
        print(f"{'ID':<5} | {'Title':<30} | {'Author':<20} | {'ISBN':<13} | {'Year':<6} | {'Qty':<4}")
        print("-" * 88)
        for b in books:
            title = b.title[:27] + "..." if len(b.title) > 30 else b.title
            author = b.author[:17] + "..." if len(b.author) > 20 else b.author
            print(f"{b.id:<5} | {title:<30} | {author:<20} | {b.isbn:<13} | {b.publication_year:<6} | {b.quantity:<4}")
