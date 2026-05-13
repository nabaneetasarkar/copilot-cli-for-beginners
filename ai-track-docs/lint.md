# Static Analysis / Lint

## Tool

**ruff** (v0.15+) — fast Python linter and formatter.

## How to Run

```powershell
cd samples/book-app-project
python -m ruff check .
```

To auto-fix:
```powershell
python -m ruff check . --fix
```

## Configuration

Defined in `samples/book-app-project/pyproject.toml`:

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "W", "F", "I", "S", "B", "UP", "RUF"]
```

### Rule Sets

| Code | Category | What it catches |
|---|---|---|
| **E** | pycodestyle errors | Line length, whitespace |
| **W** | pycodestyle warnings | Trailing whitespace, blank lines |
| **F** | pyflakes | Unused imports, undefined names |
| **I** | isort | Import ordering |
| **S** | bandit/security | Hardcoded passwords, exec, eval |
| **B** | flake8-bugbear | Common bugs, mutable default args |
| **UP** | pyupgrade | Deprecated syntax (`typing.List` → `list`) |
| **RUF** | ruff-specific | Stale `noqa`, ambiguous characters |

### Per-file Suppressions

| File pattern | Suppressed | Reason |
|---|---|---|
| `bench_find.py` | E402, T20 | Imports after sys.path; print for benchmark output |
| `book_app.py` | T20 | CLI entry point — print is the UI |
| `utils.py` | T20 | UI helper — print is intentional |
| `tests/*` | E402, S101 | Imports after sys.path; assert is the pytest idiom |

## Issues Fixed

### Crawl Ex 14

| # | Rule | File | Fix |
|---|---|---|---|
| 1 | E501 | books.py | Broke 6 long log lines across multiple lines |
| 2 | F401 | bench_find.py | Removed unused `json` import |
| 3 | I001 | books.py, book_app.py, test_books.py, bench_find.py | Sorted imports |

### Walk Ex 14 — Tightened Path: books.py (core library)

| # | Rule | File | Fix |
|---|---|---|---|
| 1 | UP035/UP006 | books.py | `typing.List` → `list`, removed `from typing` import |
| 2 | UP045 | books.py | `Optional[Book]` → `Book \| None` |
| 3 | UP015 | books.py | Removed unnecessary `"r"` mode in `open()` |
| 4 | UP024 | books.py | Replaced deprecated `IOError` with `OSError` |
| 5 | RUF100 | test_books.py | Removed 4 stale `# noqa: E402` (already suppressed in config) |
