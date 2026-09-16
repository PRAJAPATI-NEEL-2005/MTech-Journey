# Library Management - N-Tier Architecture Assignment

This is a simple Library Management application built in Python to demonstrate a strict 3-tier architecture. It operates via a lightweight Web UI using Flask.

## How to Run the Application

1. Open a terminal/command prompt.
2. Navigate to the folder containing `main.py`.
3. Install the required dependency (Flask):
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```
5. Open your web browser and navigate to: `http://127.0.0.1:5000`

## Running Tests

### Unit Tests
To run the unit tests for the business logic tier (which uses a mocked in-memory data store):
```bash
python -m unittest discover tests
```

### Swap Test
To verify that the application can switch between an SQLite database and an In-Memory data store without changing any business logic:
```bash
python swap_test.py
```

## Architecture & Tier Descriptions

The application is cleanly divided into three layers, each with strict responsibilities:

1. **/presentation (Presentation Tier)**
   - **Files:** `web_app.py`, `templates/`, `static/`
   - **Role:** Handles all User Input and Output. It runs a Flask web server, serves HTML/CSS to the browser, and routes HTTP requests.
   - **Rule:** It has zero business logic and does *not* talk to the database. It only communicates with the `BookManager` in the business tier.

2. **/business (Business Logic Tier)**
   - **Files:** `book_manager.py`, `models.py`, `exceptions.py`
   - **Role:** The brain of the application. Enforces all business rules (e.g., negative quantity, invalid ISBN, publication year not in the future).
   - **Rule:** It is completely isolated from the UI and the database. It relies on a `BookRepository` interface. It does not import `sqlite3`.

3. **/data (Data Access Tier)**
   - **Files:** `book_repository.py` (Interface), `sqlite_repository.py`, `memory_repository.py`
   - **Role:** Handles Create, Read, Update, and Delete (CRUD) operations.
   - **Rule:** It has no validation logic and no UI code. It simply executes SQL queries or array operations and returns `Book` domain models.

## Design Decision

**I used a repository interface (`BookRepository`) so I could swap SQLite for an in-memory store during testing.**
By creating an abstract base class `BookRepository` that both `SQLiteRepository` and `MemoryRepository` inherit from, the Business Logic (`BookManager`) only needs to know about the abstract interface, not the concrete implementation. This is an application of the Dependency Inversion Principle. It allowed me to write unit tests for the business logic that execute in milliseconds (because they use `MemoryRepository` instead of writing to a real disk-based database) and proves that the layers are loosely coupled.
