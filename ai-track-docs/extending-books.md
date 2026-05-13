# Extending the Books Module

This guide explains how to add new functionality to `samples/book-app-project/books.py`.

## Architecture

```
books.py          — Book dataclass + BookCollection (data layer)
book_app.py       — CLI handlers that call BookCollection methods
utils.py          — Menu display and user input helpers
tests/test_books.py — pytest tests for BookCollection
data.json         — JSON persistence file (auto-managed)
```

## How to Add a New Feature

### 1. Add a method to `BookCollection`

All data operations live in `BookCollection`. Follow the existing pattern:

```python
def your_new_method(self, ...) -> ReturnType:
    """Describe what it does."""
    # ... logic ...
    self.save_books()  # call this if you mutate self.books
    return result
```

### 2. Add a test

Add a test function in `tests/test_books.py`. The `use_temp_data_file` fixture runs automatically — no setup needed:

```python
def test_your_new_method():
    collection = BookCollection()
    collection.add_book("Title", "Author", 2024)
    result = collection.your_new_method(...)
    assert result == expected
```

### 3. Wire it into the CLI (optional)

Add a `handle_*` function in `book_app.py` and a menu option in `utils.py`.

### 4. Run tests

```powershell
cd samples/book-app-project
python -m pytest tests/ -v
```

## Key Conventions

- **Title lookups are case-insensitive** — always compare with `.lower()`
- **Mutations auto-save** — call `self.save_books()` after changing `self.books`
- **Tests are isolated** — each test gets a fresh temp data file via the `monkeypatch` fixture
