# Security & Secrets Hygiene

## What Was Checked (Ex 8)

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
