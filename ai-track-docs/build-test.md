# Build & Test

## Prerequisites

```powershell
python -m pip install pytest pytest-cov
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

## Coverage (Walk Ex 2)

### Run Tests with Coverage

```powershell
cd samples/book-app-project
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

### Baseline Coverage (Walk Ex 2)

| File | Stmts | Miss | Cover | Missing |
|---|---|---|---|---|
| books.py | 85 | 5 | **94%** | 50-51, 82, 115, 163 |
| tests/test_books.py | 96 | 0 | **100%** | — |
| book_app.py | 57 | 57 | 0% | (CLI — not unit tested) |
| utils.py | 27 | 27 | 0% | (UI helpers — not unit tested) |
| bench_find.py | 34 | 34 | 0% | (benchmark script) |
| **TOTAL** | **299** | **123** | **59%** | |

**Target module (`books.py`): 94% coverage**

### PR Coverage Snippet Template

Copy this into your PR description and fill in the numbers:

```markdown
## Coverage
| File | Cover | Change |
|---|---|---|
| books.py | 94% | ±0% |
| TOTAL | 59% | ±0% |

Command: `python -m pytest tests/ -v --cov=. --cov-report=term-missing`
```

## Local Validation Script (Ex 10)

Run all checks with a single command from the repo root:

```powershell
python validate.py
```

## CI — Soft Gating (Walk Ex 10)

A GitHub Actions workflow runs automatically on every PR that touches `samples/book-app-project/`.

### What it does

| Step | Tool | Purpose |
|---|---|---|
| Tests + Coverage | pytest + pytest-cov | Runs test suite, reports coverage % |
| Lint | ruff | Checks code style and security rules |
| Security | bandit | Scans source for security issues |
| Summary | GITHUB_STEP_SUMMARY | Posts results to the Actions job summary |

### Key design: non-blocking

- `continue-on-error: true` on every step and the job itself
- The workflow **never blocks merges** — it only surfaces evidence
- Results appear in the **Actions tab → job summary** on each PR

### Workflow file

`.github/workflows/book-app-evidence.yml`

### Viewing results

1. Open a PR that changes files in `samples/book-app-project/`
2. Go to the **Actions** tab or the **Checks** section of the PR
3. Click the workflow run → view the **Summary** section for test/lint/security output

This runs every test suite and prints a summary. Exit code is 0 if all pass, 1 if any fail. New checks can be added to the `CHECKS` list in `validate.py`.
- Python path: `C:\Users\nsarkar\AppData\Local\Python\pythoncore-3.14-64\python.exe` (if `python` isn't on PATH, use the full path)
