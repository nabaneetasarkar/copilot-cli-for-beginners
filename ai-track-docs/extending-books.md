# Extending the Books Module

This guide explains how to add new functionality to `samples/book-app-project/books.py`.

## Architecture

```
books.py          — Book dataclass + BookCollection (data layer)
book_app.py       — CLI handlers that delegate to BookCollection + utils
utils.py          — Input helpers (get_book_details, get_title_input,
                     get_author_input) + display helpers (format_book_list)
tests/test_books.py — pytest tests for BookCollection and utils
data.json         — JSON persistence file (auto-managed)
```

### Input Flow (Run Ex 3 refactor)

CLI input handling is centralized in `utils.py`. The CLI layer (`book_app.py`)
delegates to these helpers instead of calling `input()` directly:

```
book_app.handle_add()   → utils.get_book_details()
book_app.handle_remove() → utils.get_title_input()
book_app.handle_find()   → utils.get_author_input()
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

## Contract Tests

Two boundaries are validated by contract tests. If you change the shape of either, update the corresponding tests.

### Boundary 1: JSON Serialization (Golden File)

The persistence boundary between `BookCollection.save_books()` and `data.json`.

| Test | What it validates |
|---|---|
| `test_save_produces_golden_json` | Output matches `tests/golden/books_snapshot.json` |
| `test_load_roundtrip_from_golden` | Loading golden file produces correct `Book` objects |
| `test_golden_schema_keys` | Each entry has exactly `{title, author, year, read}` |

**When to update:** Only when you change `Book` dataclass fields or JSON format.

**How to update:**
1. Make your change to `books.py`
2. Run tests — contract tests will fail with a clear diff
3. Regenerate golden file:
   ```powershell
   cd samples/book-app-project
   python -c "
   from books import Book
   from dataclasses import asdict
   import json
   books = [
       Book(title='Dune', author='Frank Herbert', year=1965, read=True),
       Book(title='1984', author='George Orwell', year=1949, read=False),
   ]
   print(json.dumps([asdict(b) for b in books], indent=2))
   " > tests/golden/books_snapshot.json
   ```
4. Re-run tests, include golden file update in your PR

### Boundary 2: `stats()` API + Display Format

The interface between the data layer (`BookCollection.stats()`) and any consumer, plus the display format contract for `format_book_list`.

| Test | What it validates |
|---|---|
| `test_stats_contract_keys` | Returns exactly `{total_books, read, unread, unique_authors}` |
| `test_stats_contract_types` | All values are `int` |
| `test_stats_contract_values` | Invariant: `total == read + unread` |
| `test_format_book_list_contract_line_pattern` | Each line matches `N. Title by Author (YYYY) - Read\|Unread` |

**When to update:** When you add/remove keys from `stats()` or change the display format.

**How to update:** Adjust the expected keys/pattern in the test, document the change in your PR.
