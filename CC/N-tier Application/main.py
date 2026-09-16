import os
from data.sqlite_repository import SQLiteRepository
from business.book_manager import BookManager
from presentation.web_app import WebApp

def main():
    print("Starting N-Tier Library Management System...")
    
    # 1. Initialize the Data Tier (Database)
    repository = SQLiteRepository(db_path="library.db")
    
    # 2. Initialize the Business Logic Tier
    book_manager = BookManager(repository)
    
    # 3. Initialize the Presentation Tier (Web UI)
    app = WebApp(book_manager)
    
    # Start the web application
    print("Starting Web Server on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)

if __name__ == "__main__":
    main()
