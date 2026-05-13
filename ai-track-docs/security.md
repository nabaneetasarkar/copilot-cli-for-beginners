# Security & Secrets Hygiene

## Security Scanning (Walk Ex 8)

### Tools

| Tool | Purpose | How to Run |
|---|---|---|
| **Ruff (S rules)** | Inline security linting (flake8-bandit) | `ruff check .` |
| **Bandit** | Python security scanner | `bandit -r books.py book_app.py utils.py` |
| **pip-audit** | Dependency vulnerability check | `pip-audit` |

### Running All Scans

```powershell
cd samples/book-app-project

# Lint (includes security rules)
python -m ruff check .

# Security scan (source only, exclude tests)
python -m bandit -r books.py book_app.py utils.py

# Dependency vulnerabilities
python -m pip_audit
```

### Configuration

- **Ruff**: `S` (flake8-bandit) rules enabled in `pyproject.toml` `[tool.ruff.lint]`
- **S101 suppressed in tests** — `assert` is expected in test files (`tests/*` → `S101` ignored)
- **Bandit** declared as dev dependency in `pyproject.toml`

### Scan Results (Walk Ex 8)

| Scan | Result |
|---|---|
| Ruff (E/W/F/I/S) | All checks passed |
| Bandit (source files) | No issues identified |
| pip-audit | No known vulnerabilities found |

### Scan Results (Run Ex 8)

| Scan | Result |
|---|---|
| Ruff (E/W/F/I/S/B/UP/RUF) | All checks passed |
| Bandit `-r . -ll --exclude ./tests` | No issues identified (371 lines scanned) |

## Hardening Applied (Run Ex 8)

### 1. Schema validation on `load_books`

Unknown keys in `data.json` records are silently stripped before constructing `Book` objects. Only `{title, author, year, read}` are accepted. A warning log is emitted for each record with extra keys.

- **Risk mitigated:** Data injection via tampered/corrupted JSON files
- **Side effects:** None — existing valid data files are unaffected
- **Constant:** `_BOOK_KEYS = frozenset({"title", "author", "year", "read"})`

### 2. File size limit on `load_books`

Loading is refused if `data.json` exceeds `MAX_DATA_FILE_BYTES` (default 10 MB). The collection starts empty and a warning is printed + logged.

- **Risk mitigated:** Memory exhaustion from maliciously large data files
- **Side effects:** None — normal data files are orders of magnitude smaller
- **Constant:** `MAX_DATA_FILE_BYTES = 10 * 1024 * 1024`
- **Override:** Not configurable via env var (hardcoded safety limit)

### 3. Year upper bound in `add_book`

`add_book()` now rejects years exceeding `MAX_YEAR` (9999) with `ValueError`.

- **Risk mitigated:** Absurd/unbounded integer values in data
- **Side effects:** None — no valid book has a year > 9999
- **Constant:** `MAX_YEAR = 9999`

### Tests Added

| Test | Validates |
|---|---|
| `test_year_upper_bound_rejected` | Year > MAX_YEAR raises ValueError |
| `test_year_at_max_accepted` | Year == MAX_YEAR succeeds |
| `test_load_rejects_oversized_file` | Oversized data.json → empty collection |
| `test_load_strips_unknown_keys` | Extra JSON keys stripped, Book created normally |

### Justified Suppression

| Rule | File | Justification |
|---|---|---|
| S101 (assert) | `tests/*` | Standard pytest pattern; asserts are the test mechanism |

## Secrets Hygiene (Crawl Ex 8)

### What Was Checked

| Area | Status | Notes |
|---|---|---|
| `.env` files | Already covered | `.env`, `.env.local`, `.env.*.local` in `.gitignore` |
| Key/cert files | Added | `*.pem`, `*.key`, `*.crt`, `*.p12`, `*.pfx`, `*.jks` |
| SSH keys | Added | `id_rsa*`, `id_ed25519*` |
| Credential files | Added | `.credentials`, `*.secret`, `*.keystore` |
| Python venvs | Added | `venv/`, `.venv/`, `*.egg-info/` |
| Hardcoded secrets in code | None found | Grep for `password`, `secret`, `token`, `api_key` — clean |
| `SECURITY.md` | Exists | GitHub's standard disclosure policy — no changes needed |

## .gitignore Improvements Made

Added patterns for:
- Private keys and certificates (`*.pem`, `*.key`, `*.crt`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`)
- SSH keys (`id_rsa*`, `id_ed25519*`)
- Credential files (`.credentials`, `*.secret`)
- Python virtual environments (`venv/`, `.venv/`, `*.egg-info/`)

## Guidelines

- **Never commit secrets** — use environment variables or a secrets manager
- **Review diffs** before committing to catch accidental credential inclusion
- **If a secret is committed:** rotate it immediately, then use `git filter-branch` or BFG to purge history
