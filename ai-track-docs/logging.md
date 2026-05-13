# Logging

## Overview

Structured JSON logs are emitted from `books.py` using Python's `logging` module. Each log entry contains consistent fields for easy filtering and debugging.

## Log Fields

| Field | Type | Description |
|---|---|---|
| `op` | string | Operation name (`load_books`, `add_book`, `remove_book`, `mark_as_read`, `find_by_author`, `stats`) |
| `status` | string | Outcome (`ok`, `not_found`, `no_file`, `corrupt_file`, `error`) |
| `elapsed_ms` | float | Wall-clock time in milliseconds (timed operations) |
| `title` | string | Book title (when applicable) |
| `author` | string | Author name (for `find_by_author`) |
| `count` | int | Number of books loaded (for `load_books`) |
| `matches` | int | Number of results (for `find_by_author`) |
| `total_books` | int | Collection size (for `stats`) |
| `read` | int | Read count (for `stats`) |
| `unread` | int | Unread count (for `stats`) |
| `unique_authors` | int | Distinct author count (for `stats`) |

## How to View Logs Locally

By default, Python's logging module doesn't output anything unless configured. To see the structured logs, run the app with logging enabled:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

Or from the command line:

```powershell
cd samples/book-app-project
python -c "import logging; logging.basicConfig(level=logging.INFO); from books import BookCollection; c = BookCollection(); c.add_book('Test', 'Author', 2024)"
```

Example output:
```
INFO:books:{"op": "load_books", "status": "no_file", "count": 0}
INFO:books:{"op": "add_book", "status": "ok", "title": "Test", "elapsed_ms": 0.42}
```

## Instrumented Operations

- `load_books` — logged on init (ok / no_file / corrupt_file) with timing
- `add_book` — logged after successful add with timing
- `remove_book` — logged with ok or not_found status, with timing
- `mark_as_read` — logged with ok or not_found status
- `find_by_author` — logged with match count
- `stats` — logged with total/read/unread/unique_authors metrics

## Verification

Run this to see all log events:

```powershell
cd samples/book-app-project
python -c "
import logging, tempfile, os
logging.basicConfig(level=logging.INFO, format='%(name)s %(levelname)s %(message)s')
import books
tf = tempfile.mkdtemp()
books.DATA_FILE = os.path.join(tf, 'data.json')
c = books.BookCollection()
c.add_book('Dune', 'Frank Herbert', 1965)
c.mark_as_read('Dune')
c.find_by_author('Frank Herbert')
print(c.stats())
import shutil; shutil.rmtree(tf, ignore_errors=True)
"
```

Expected output includes structured JSON log lines for each operation.
