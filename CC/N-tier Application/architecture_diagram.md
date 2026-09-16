# Architecture Diagram

This diagram illustrates the 3-tier architecture of our Library Management application.

## ASCII Diagram (For Plain Text Viewing)

```text
+-------------------------+
|    Presentation Tier    |
|   (Flask Web Server)    |
+-------------------------+
             |
             v  Calls methods & passes user input
+-------------------------+
|   Business Logic Tier   |
| (Book Manager / Models) |
+-------------------------+
             |
             v  Uses Interface (no direct DB calls)
+-------------------------+
|     Data Access Tier    |
|  (SQLite / In-Memory)   |
+-------------------------+
             |
             v  Executes SQL Queries
+-------------------------+
|        Database         |
|      (library.db)       |
+-------------------------+
```

## Mermaid Diagram (For GitHub / Markdown Viewers)


```mermaid
graph TD
    %% Tiers
    subgraph Presentation Tier
        Web[Web Application<br>main.py, presentation/web_app.py]
        UI[Browser UI<br>HTML / CSS Templates]
    end

    subgraph Business Logic Tier
        BM[Book Manager<br>business/book_manager.py]
        Models[Domain Models & Exceptions<br>business/models.py, exceptions.py]
    end

    subgraph Data Access Tier
        RepoInterface{BookRepository Interface<br>data/book_repository.py}
        SQLiteRepo[SQLite Repository<br>data/sqlite_repository.py]
        MemRepo[Memory Repository<br>data/memory_repository.py]
        DB[(SQLite Database<br>library.db)]
    end

    %% Data Flow & Dependencies
    UI <-->|HTTP Requests/Responses| Web
    Web -->|Calls methods, handles routing| BM

    BM -->|Validates rules, coordinates| RepoInterface
    BM -.->|Uses| Models
    RepoInterface <|-- SQLiteRepo : Implements
    RepoInterface <|-- MemRepo : Implements
    SQLiteRepo -->|Reads/Writes SQL| DB

    %% Styling
    classDef presentation fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef business fill:#cce5ff,stroke:#007bff,stroke-width:2px;
    classDef data fill:#f8d7da,stroke:#dc3545,stroke-width:2px;
    classDef interface fill:#fff3cd,stroke:#ffc107,stroke-width:2px,stroke-dasharray: 5 5;

    class CLI presentation;
    class BM,Models business;
    class SQLiteRepo,MemRepo,DB data;
    class RepoInterface interface;
```

## Data Flow Summary
1.  **User Input**: The user interacts with the `presentation/cli.py`.
2.  **Validation & Logic**: The CLI passes data to the `business/book_manager.py`, which validates the rules (e.g., negative quantity, invalid ISBN).
3.  **Data Persistence**: If validation passes, the `BookManager` calls a method on the `BookRepository` interface. At runtime, this interface is backed by `SQLiteRepository` which saves the data to the `library.db` database.
