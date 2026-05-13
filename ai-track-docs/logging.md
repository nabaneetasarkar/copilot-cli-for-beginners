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

### books.py (data layer)

- `load_books` — logged on init (ok / no_file / corrupt_file / file_too_large / unknown_keys) with timing
- `save_books` — logged on retry / ok_after_retry / error
- `add_book` — logged after successful add with timing
- `remove_book` — logged with ok or not_found status, with timing
- `mark_as_read` — logged with ok or not_found status
- `find_by_author` — logged with match count
- `stats` — logged with total/read/unread/unique_authors metrics

### book_app.py (CLI layer)

- `cli_dispatch` — logged on every command invocation (command name); warns on unknown commands
- `cli_list` — logged with count + elapsed_ms
- `cli_add` — logged on success (title) or validation_error (error message)
- `cli_remove` — logged with ok/not_found + title
- `cli_find` — logged with author + match count

### utils.py (input layer)

- `get_book_details` — logged with parsed title/author/year; warns on invalid year input

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

## Instrumentation Coverage (Run Ex 9)

| File | Logger | Ops Logged | Layer |
|---|---|---|---|
| `books.py` | `books` | load, save, add, remove, mark_as_read, find_by_author, stats | Data |
| `book_app.py` | `book_app` | cli_dispatch, cli_list, cli_add, cli_remove, cli_find | CLI |
| `utils.py` | `utils` | get_book_details | Input |

### Consistent field conventions

All log entries across all files use the same JSON structure:

| Field | Required | Notes |
|---|---|---|
| `op` | Yes | Prefixed by layer: `load_books`, `cli_list`, `get_book_details` |
| `status` | Yes | `ok`, `not_found`, `error`, `validation_error`, `invalid_year`, etc. |
| `elapsed_ms` | When timed | Wall-clock ms, rounded to 2 decimals |
| domain fields | As needed | `title`, `author`, `count`, `matches`, `command`, `error` |

### Validation: full folder sweep

To verify logging works across all 3 files:

```powershell
cd samples/book-app-project
python -c "
import logging, sys
logging.basicConfig(level=logging.INFO, format='%(name)s %(levelname)s %(message)s')
# 1. Data layer (books.py)
import tempfile, os, books
tf = tempfile.mkdtemp()
books.DATA_FILE = os.path.join(tf, 'data.json')
c = books.BookCollection()
c.add_book('Dune', 'Frank Herbert', 1965)
c.mark_as_read('Dune')
c.find_by_author('Frank Herbert')
c.stats()
# 2. CLI layer (book_app.py)
import book_app
book_app.collection = c
book_app.handle_list()
# Cleanup
import shutil; shutil.rmtree(tf, ignore_errors=True)
"
```

Expected: structured JSON log lines from `books`, `book_app`, and `utils` loggers.
