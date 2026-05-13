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
select = ["E", "W", "F", "I"]
```

- **E** — pycodestyle errors (line length, whitespace)
- **W** — pycodestyle warnings
- **F** — pyflakes (unused imports, undefined names)
- **I** — isort (import ordering)

### Per-file Ignores

- `bench_find.py` and `tests/*` — E402 suppressed (imports after `sys.path` manipulation are intentional)

## Issues Fixed (Ex 14)

| # | Rule | File | Fix |
|---|---|---|---|
| 1 | E501 | books.py | Broke 6 long log lines across multiple lines |
| 2 | F401 | bench_find.py | Removed unused `json` import |
| 3 | I001 | books.py, book_app.py, test_books.py, bench_find.py | Sorted imports |
