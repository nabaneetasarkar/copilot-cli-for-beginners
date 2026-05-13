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

## Entry Points

| Entry Point | Language | What It Does |
|---|---|---|
| `samples/book-app-project/book_app.py` | Python | CLI menu — add/list/find/remove/mark-read books |
| `samples/src/index.js` | JavaScript | Central module entry for JS sample code |
| `package.json` scripts | Node | `generate:headers`, `scan:demos`, `create:tapes`, etc. |

## Test Approach

- **Python:** pytest — tests live in `samples/book-app-project/tests/test_books.py`
  - Uses `tmp_path` + `monkeypatch` fixtures to isolate the data file
  - Covers: add, remove, mark-as-read, and negative cases
- **JavaScript:** No test framework currently configured for `samples/src/`
- **Run tests:** `cd samples/book-app-project && python -m pytest tests/`

## Low-Risk Module Candidates

| # | Module | Why Low Risk |
|---|---|---|
| 1 | `samples/book-app-project/books.py` | Pure data logic (CRUD on a list of books). Has existing tests. No I/O beyond a JSON file. Changes are easy to verify. |
| 2 | `samples/book-app-project/utils.py` | UI helper functions only (print menu, get input). No side effects on data. |
| 3 | `samples/src/utils/helpers.js` | Standalone JS utility. No dependencies on other modules. |

## Chosen Module

**`samples/book-app-project/books.py`** (`BookCollection` class + `Book` dataclass)

**Why:** It has existing pytest coverage, contains pure data logic (add, remove, find, mark-as-read), and changes are immediately testable. It's isolated from the CLI layer (`book_app.py`) so modifications won't break user-facing flows. This makes it the safest place to experiment across the remaining exercises.
