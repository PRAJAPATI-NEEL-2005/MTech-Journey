# Project Explanation: N-Tier Library Management Application

This document explains the entire process of how we built this application, the decisions we made, and what every file in the project does.

## What We Built

We built a 3-tier architecture application called "Library Management". The goal was to demonstrate **Separation of Concerns**, meaning different parts of the application should have strictly separated responsibilities.

We initially built it as a Command Line Interface (CLI), and later upgraded it to a Web UI using Flask. Because we strictly followed the N-tier architecture, upgrading the UI did not require us to change *any* of our core business logic or database code!

## The Three Tiers Explained

### 1. The Data Access Tier (`/data`)
**Responsibility:** Talking to the database. It doesn't care about business rules (like whether an ISBN is valid); it only cares about saving and retrieving data.

* **`data/book_repository.py`**: This is an "Interface" (an Abstract Base Class). It defines the methods (`add_book`, `get_all_books`, etc.) that any database implementation must have.
* **`data/sqlite_repository.py`**: This is the real database logic. It uses Python's built-in `sqlite3` to execute SQL queries (like `SELECT`, `INSERT`, `UPDATE`). It takes rows from the database and turns them into `Book` objects.
* **`data/memory_repository.py`**: This is a fake, in-memory database using a simple Python list (`[]`). We created this so we could test our application instantly without needing to create or modify a real database file.

### 2. The Business Logic Tier (`/business`)
**Responsibility:** The "Brain" of the application. It validates all incoming data, enforces rules, and tells the Data Tier what to save. It is completely unaware of *how* the user is interacting with the app (Web vs. CLI) and unaware of *how* data is being saved (SQLite vs. Memory).

* **`business/models.py`**: Contains the `Book` dataclass. This is just a simple object that holds data (title, author, isbn, etc.) to pass around the application.
* **`business/exceptions.py`**: Contains custom error types (like `ValidationError` or `OutOfStockError`). Using custom exceptions makes it easy to catch specific errors.
* **`business/book_manager.py`**: This is the core logic engine. When you try to add a book, it checks if the title is empty, if the year is in the future, if the ISBN is 10 or 13 digits, and if the quantity is negative. If everything passes, it passes the data to the Data layer.

### 3. The Presentation Tier (`/presentation`)
**Responsibility:** Interacting with the user. It handles button clicks, form submissions, and displays data on the screen. It doesn't validate data rules or talk to the database directly.

* **`presentation/web_app.py`**: This uses the **Flask** web framework. It defines URLs (like `/add` or `/delete/<id>`). When a user submits an HTML form, this file grabs that data and passes it directly to the `BookManager`.
* **`presentation/templates/index.html`**: The HTML skeleton. It uses Jinja templates (the `{{ }}` syntax) to loop through the books and display them in a table.
* **`presentation/static/style.css`**: The design rules that make the application look modern and clean.

## Other Essential Files

* **`main.py`**: The entry point. This file glues the 3 tiers together. It creates the Database, passes the Database into the Business Manager, passes the Business Manager into the Web App, and then starts the server.
* **`swap_test.py`**: The ultimate proof that our architecture works. This script runs the application logic twice: once using SQLite, and once using the in-memory list. It proves the Business tier doesn't care what database it uses.
* **`tests/test_business_logic.py`**: Contains automated Unit Tests. It rapidly feeds bad data (like negative quantities or fake ISBNs) into the `BookManager` to mathematically prove that our validation rules are working.
* **`requirements.txt`**: A list of external libraries required to run the code (in this case, just `Flask`).
* **`architecture_diagram.md`**: Visualizes how data flows from the Web UI, down to the Business Layer, and finally into the Database.
