# System Overview

## Architecture Diagram

See [architecture.mmd](architecture.mmd) for the full component map with real file paths and data flows.

## Repository

- **Repo:** copilot-cli-for-beginners
- **Purpose:** A hands-on GitHub Copilot CLI course — 7 chapters of Markdown lessons + sample apps
- **Primary languages:** Markdown (course content), Python (book app), JavaScript (sample modules)
- **Structure:**
  - `00-quick-start/` through `07-putting-it-together/` — course chapters (Markdown)
  - `samples/book-app-project/` — Python book collection CLI app (the main sample)
  - `samples/book-app-buggy/` — intentionally buggy variant for debugging exercises
  - `samples/src/` — JavaScript modules (api, auth, components, models, services, utils)
  - `samples/buggy-code/` — buggy JS/Python snippets for practice
  - `samples/agents/`, `samples/skills/`, `samples/mcp-configs/` — Copilot config examples
  - `.github/scripts/` — build tooling (header generation, demo GIF pipeline)
  - `ai-track-docs/` — engineering track documentation (16 files)

## Book App Subsystem (`samples/book-app-project/`)

### File Map

| File | Role | Key Responsibilities |
|---|---|---|
| `books.py` | Data layer | `Book` dataclass, `BookCollection` (CRUD, persistence, search, stats) |
| `book_app.py` | CLI entry point | Command routing (`list`, `add`, `remove`, `find`, `help`) |
| `utils.py` | Input/display helpers | `get_book_details()`, `get_title_input()`, `get_author_input()`, `format_book_list()` |
| `bench_find.py` | Benchmark | Micro-benchmark for `find_book_by_title` O(1) lookup |
| `data.json` | Persistence | Auto-managed JSON file (never edit manually) |
| `pyproject.toml` | Config | Dependencies, ruff lint rules (8 rule sets), pytest config |
| `tests/test_books.py` | Test suite | 24 tests, 100% test file coverage |
| `tests/golden/books_snapshot.json` | Contract fixture | Golden file for JSON serialization contract |

### Data Flow

```
User → book_app.py (CLI) → utils.py (input) → BookCollection (logic) → data.json (disk)
                          ← utils.py (display) ← BookCollection      ← data.json
```

### BookCollection API

| Method | Returns | Side Effects | Resilience |
|---|---|---|---|
| `add_book(title, author, year)` | `Book` | Saves to disk | Retry with backoff |
| `remove_book(title)` | `bool` | Saves to disk | Retry with backoff |
| `mark_as_read(title)` | `bool` | Saves to disk | Retry with backoff |
| `find_book_by_title(title)` | `Book \| None` | None | O(1) dict lookup |
| `find_by_author(author)` | `list[Book]` | None | Linear scan |
| `list_books()` | `list[Book]` | None | — |
| `stats()` | `dict` | None | — |
| `load_books()` | None | Reads from disk | Handles corrupt/missing files |
| `save_books()` | None | Atomic write to disk | 3 retries, exponential backoff |

### Feature Flags

| Flag | Default | Effect |
|---|---|---|
| `BOOK_APP_CASE_SENSITIVE` | OFF | Title lookups require exact case when ON |
| `BOOK_APP_STRICT_VALIDATION` | OFF | Duplicate titles rejected when ON |

See [feature-flags.md](feature-flags.md) for lifecycle details.

### Resilience

- **Atomic write:** temp file + `os.replace()` — crash never corrupts `data.json`
- **Retry:** `save_books()` retries 3 times with 0.1s exponential backoff on `OSError`
- **Corrupt file recovery:** `load_books()` gracefully handles malformed JSON

See [resilience.md](resilience.md) for tuning and failure test details.

### Observability

All 6 operations emit structured JSON logs via `logging.getLogger(__name__)`:
- `load_books`, `save_books`, `add_book`, `remove_book`, `mark_as_read`, `find_by_author`
- Timing: `elapsed_ms` on `add_book`, `remove_book`, `load_books`

See [logging.md](logging.md) for log schemas.

### Static Analysis

8 ruff rule sets: E, W, F, I, S, B, UP, RUF. T20 (print) suppressed for CLI files.

See [lint.md](lint.md) for rule table and suppression docs.

### Security

`bandit` scans configured. S101 (assert) suppressed in tests only.

See [security.md](security.md) for scan details.

## Test Approach

- **Framework:** pytest 9.0.3 + pytest-cov 7.1.0
- **Test count:** 24 tests
- **Coverage:** 73% overall, 90% on `books.py`, 100% on test file
- **Isolation:** `use_temp_data_file` autouse fixture — each test gets a fresh temp `data.json`
- **Contract tests:** Golden file locks JSON serialization format
- **Run:**
  ```powershell
  cd samples/book-app-project
  python -m pytest tests/ -v --cov=. --cov-report=term-missing
  ```

See [build-test.md](build-test.md) for CI details.

## CI / CD

- **Workflow:** `.github/workflows/book-app-evidence.yml` (soft gate — non-blocking)
- **Jobs:** tests + coverage, ruff lint, bandit scan → job summary
- **PR template:** `.github/PULL_REQUEST_TEMPLATE.md` with review focus + reviewer checklist

## Documentation Index

| Doc | Purpose |
|---|---|
| [SYSTEM-OVERVIEW.md](SYSTEM-OVERVIEW.md) | This file — subsystem map |
| [extending-books.md](extending-books.md) | How to add features + golden file guide |
| [architecture.mmd](architecture.mmd) | Mermaid component diagram |
| [delegation-checklist.md](delegation-checklist.md) | 7-step delegation workflow |
| [evidence-guide.md](evidence-guide.md) | Evidence capture patterns for PRs |
| [feature-flags.md](feature-flags.md) | Flag lifecycle + ON/OFF validation |
| [resilience.md](resilience.md) | Retry/backoff behavior + failure tests |
| [logging.md](logging.md) | Structured log schemas for all operations |
| [lint.md](lint.md) | Ruff rule sets + suppression docs |
| [security.md](security.md) | Bandit scan + security guidance |
| [build-test.md](build-test.md) | CI workflow docs |
| [perf-baseline.md](perf-baseline.md) | Benchmark results for find_book_by_title |
| [dependencies.md](dependencies.md) | Dependency versions + upgrade notes |
| [pr-conventions.md](pr-conventions.md) | PR review focus guide |
| [onboarding-prompt.md](onboarding-prompt.md) | New contributor quick start |
| [BACKLOG-EX12.md](BACKLOG-EX12.md) | Epic with 5 backlog items |

## Risk Notes

| Risk | Mitigation | File |
|---|---|---|
| `data.json` corruption | Atomic write + corrupt file recovery | `books.py` L43-69 |
| Disk full / I/O error | Retry with backoff (3 attempts) | `books.py` L77-120 |
| Feature flag drift | Flags default OFF; lifecycle doc enforces retire step | `feature-flags.md` |
| Stale docs | This overview links to all docs; review on each PR | This file |
| Breaking JSON schema | Golden file contract test catches regressions | `tests/golden/` |
| Lint rule gaps | 8 rule sets enabled; suppressions justified in lint.md | `pyproject.toml` |
