import os
from data.sqlite_repository import SQLiteRepository
from data.memory_repository import MemoryRepository
from business.book_manager import BookManager

def run_test_with_repository(repo_name, repository):
    print(f"--- Running tests with {repo_name} ---")
    
    # The business layer doesn't know or care what repository it receives
    manager = BookManager(repository)
    
    # 1. Add a book
    print("Adding a book...")
    book = manager.add_book("Clean Architecture", "Robert C. Martin", "0134494164", 2017, 3)
    print(f"Added book with ID: {book.id}")
    
    # 2. View all books
    books = manager.view_all_books()
    print(f"Total books in library: {len(books)}")
    
    # 3. Check out a book
    print("Checking out the book...")
    manager.check_out_book(book.id)
    
    # 4. View updated quantity
    updated_book = manager.get_book(book.id)
    print(f"Updated quantity: {updated_book.quantity}")
    
    print(f"--- Completed tests for {repo_name} ---\n")

def main():
    print("=== N-Tier Architecture Swap Test ===\n")
    print("This test demonstrates that the Business Logic tier works identically")
    print("regardless of whether we use an SQLite database or an in-memory list.\n")

    # Clean up any existing test db
    db_file = "test_swap.db"
    if os.path.exists(db_file):
        os.remove(db_file)

    # 1. Run with SQLite Repository
    sqlite_repo = SQLiteRepository(db_path=db_file)
    run_test_with_repository("SQLite Repository", sqlite_repo)

    # 2. Run with Memory Repository
    memory_repo = MemoryRepository()
    run_test_with_repository("Memory Repository", memory_repo)

    # Clean up
    if os.path.exists(db_file):
        os.remove(db_file)

if __name__ == "__main__":
    main()
