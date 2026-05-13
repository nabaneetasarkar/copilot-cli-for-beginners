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
select = ["E", "W", "F", "I", "S", "B", "UP", "RUF", "C4", "SIM", "PTH", "PERF", "T20"]
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
| **C4** | flake8-comprehensions | Unnecessary list/dict/set calls |
| **SIM** | flake8-simplify | Simplifiable if/else, context managers |
| **PTH** | flake8-use-pathlib | `os.path` → `pathlib.Path` |
| **PERF** | perflint | Unnecessary list copies, slow patterns |
| **T20** | flake8-print | Stray `print()` calls |

### Per-file Suppressions

| File pattern | Suppressed | Reason |
|---|---|---|
| `bench_find.py` | E402, T20, PTH | Imports after sys.path; print for benchmark; os.path acceptable in throwaway benchmark |
| `book_app.py` | T20 | CLI entry point — print is the UI |
| `utils.py` | T20 | UI helper — print is intentional |
| `tests/*` | E402, S101 | Imports after sys.path; assert is the pytest idiom |

### Inline Suppressions

| File | Line | Rule | Reason |
|---|---|---|---|
| `books.py` | 74 | T201 | Intentional user-facing warning (oversized file, STRICT_LOAD OFF) |
| `books.py` | 111 | T201 | Intentional user-facing warning (corrupt file, STRICT_LOAD OFF) |

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

### Run Ex 14 — Added 5 rule sets + fixed 7 findings

**New rule sets:** C4 (comprehensions), SIM (simplify), PTH (pathlib), PERF (perflint), T20 (print)

| # | Rule | File | Fix |
|---|---|---|---|
| 1 | PTH202 | books.py | `os.path.getsize()` → `Path().stat().st_size` |
| 2 | PTH123 | books.py | `open(DATA_FILE)` → `Path(DATA_FILE).open()` |
| 3 | PTH120/100 | books.py | `os.path.dirname(os.path.abspath())` → `Path().resolve().parent` |
| 4 | PTH105 | books.py | `os.replace()` → `Path().replace()` |
| 5 | PTH110/108 | books.py | `os.path.exists()` / `os.unlink()` → `Path().exists()` / `.unlink()` |
| 6 | PTH120/100 | test_books.py | `os.path.dirname(os.path.abspath(__file__))` → `Path(__file__).resolve().parent` |
| 7 | PTH118/123 | test_books.py | `os.path.join()` / `open()` → `Path /` operator / `.open()` |

**Suppressed (justified):**

| Rule | Location | Reason |
|---|---|---|
| T201 | books.py L74, L111 | Intentional user-facing warnings (STRICT_LOAD OFF path) |
| PTH | bench_find.py | Throwaway benchmark — low value to convert |
