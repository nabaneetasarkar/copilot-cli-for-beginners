# Logging

## Overview

Structured JSON logs are emitted from `books.py` using Python's `logging` module. Each log entry contains consistent fields for easy filtering and debugging.

## Log Fields

| Field | Type | Description |
|---|---|---|
| `op` | string | Operation name (`load_books`, `add_book`, `remove_book`) |
| `status` | string | Outcome (`ok`, `not_found`, `no_file`, `corrupt_file`) |
| `elapsed_ms` | float | Wall-clock time in milliseconds |
| `title` | string | Book title (when applicable) |
| `count` | int | Number of books loaded (for `load_books`) |

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

- `load_books` — logged on init (ok / no_file / corrupt_file)
- `add_book` — logged after successful add
- `remove_book` — logged with ok or not_found status
