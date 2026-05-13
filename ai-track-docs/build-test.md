# Build & Test

## Prerequisites

```powershell
python -m pip install pytest
```

## Build

No build step required — the project is pure Python (no compilation).

## Run Tests

```powershell
cd samples/book-app-project
python -m pytest tests/ -v
```

### Expected Output (Ex 2 baseline)

```
tests/test_books.py::test_add_book PASSED
tests/test_books.py::test_mark_book_as_read PASSED
tests/test_books.py::test_mark_book_as_read_invalid PASSED
tests/test_books.py::test_remove_book PASSED
tests/test_books.py::test_remove_book_invalid PASSED
tests/test_books.py::test_find_book_by_title_case_insensitive PASSED

6 passed
```

## Notes

- Tests use `tmp_path` + `monkeypatch` to isolate the data file — no cleanup needed
- Python path: `C:\Users\nsarkar\AppData\Local\Python\pythoncore-3.14-64\python.exe` (if `python` isn't on PATH, use the full path)
