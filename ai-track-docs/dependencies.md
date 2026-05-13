# Dependency Notes

## Python — `samples/book-app-project/pyproject.toml`

| Dependency | Purpose | Constraint | Pinned? |
|---|---|---|---|
| Python | Runtime | `>=3.10` | Lower-bound only (acceptable) |
| pytest | Test framework | `>=9.0,<10` | Constrained (Ex 7) |

### Standard library only
The book app (`books.py`, `book_app.py`, `utils.py`) uses only standard library modules: `json`, `dataclasses`, `typing`, `sys`. No third-party runtime dependencies.

### Policy
- **pytest** is the only external dependency. It was unpinned (`"pytest"`) — updated to `"pytest>=9.0,<10"` to prevent surprise major-version breakage while still allowing patch updates.
- No `requirements.txt` exists — `pyproject.toml` is the single source of truth.

## JavaScript — root `package.json`

| Dependency | Purpose | Constraint | Pinned? |
|---|---|---|---|
| (none) | — | — | — |

No runtime or dev dependencies declared. The `package.json` only defines npm scripts for the course build tooling (header generation, demo GIF pipeline). Scripts call Python/Node directly.

`package-lock.json` exists but is empty of dependencies.

## Gaps & Observations

- No `requirements.txt` or lock file for Python — acceptable for a learning project, but in production you'd want `pip freeze > requirements.txt` or a `uv.lock`.
- No JS dependencies to audit.
- No known vulnerabilities in the dependency tree (pytest + stdlib only).
