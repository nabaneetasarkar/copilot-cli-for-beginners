# Dependency Notes

## Python — `samples/book-app-project/pyproject.toml`

| Dependency | Purpose | Section | Constraint | Installed |
|---|---|---|---|---|
| Python | Runtime | `requires-python` | `>=3.10` | 3.14.5 |
| pytest | Test framework | `[project.optional-dependencies] dev` | `>=9.0.3,<10` | 9.0.3 |
| pytest-cov | Coverage reporting | `[project.optional-dependencies] dev` | `>=7.1.0,<8` | 7.1.0 |
| ruff | Linter/formatter | `[project.optional-dependencies] dev` | `>=0.15.0,<1` | 0.15.12 |

### Install dev dependencies

```powershell
pip install -e ".[dev]"
```

### Standard library only
The book app (`books.py`, `book_app.py`, `utils.py`) uses only standard library modules: `json`, `dataclasses`, `typing`, `sys`. No third-party runtime dependencies.

### Changes (Walk Ex 7)

1. **Moved test deps to `[project.optional-dependencies] dev`** — previously listed under `[project].dependencies`, which would install pytest/pytest-cov for end users. Now they're dev-only.
2. **Tightened lower bounds** — `pytest>=9.0` → `>=9.0.3`, `pytest-cov>=7.0` → `>=7.1.0` to match tested versions.
3. **Added ruff** — was installed ad-hoc; now declared as a dev dependency (`>=0.15.0,<1`).
4. **Production dependencies = none** — `dependencies = []` makes it explicit the app has no runtime third-party deps.

### Rollback

Revert `pyproject.toml` to move deps back to `[project].dependencies` and remove `[project.optional-dependencies]`:

```toml
dependencies = ["pytest>=9.0,<10", "pytest-cov>=7.0,<8"]
```

### Policy
- `pyproject.toml` is the single source of truth (no `requirements.txt`).
- Pin lower bounds to the tested version; upper bounds prevent surprise major-version breakage.
- No known vulnerabilities in the dependency tree (all stdlib + dev-only tools).

## JavaScript — root `package.json`

| Dependency | Purpose | Constraint | Pinned? |
|---|---|---|---|
| (none) | — | — | — |

No runtime or dev dependencies declared. The `package.json` only defines npm scripts for the course build tooling (header generation, demo GIF pipeline). Scripts call Python/Node directly.

`package-lock.json` exists but is empty of dependencies.

## Gaps & Observations

- No lock file for Python — acceptable for a learning project, but in production consider `uv.lock` or `pip freeze`.
- No JS dependencies to audit.
- No known vulnerabilities in the dependency tree.
