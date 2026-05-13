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
