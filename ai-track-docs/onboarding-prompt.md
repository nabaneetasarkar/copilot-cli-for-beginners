# Onboarding Prompt — Walk Track

Use this prompt when starting a new Walk exercise with GitHub Copilot Chat. Paste it into the chat along with the exercise description.

---

## Walk Exercise Prompt Template

```
I am working on the Walk track of the AI Engineering program.

Project: book-app-project (Python CLI for managing a book collection)
Key files:
  - samples/book-app-project/books.py      — Book dataclass + BookCollection
  - samples/book-app-project/book_app.py   — CLI entry point + command handlers
  - samples/book-app-project/utils.py      — UI helper functions
  - samples/book-app-project/tests/test_books.py — pytest test suite

Conventions:
  - Branch: walk/<github-id>/ex<N>-<short-name>
  - Commit: walk: ex<N> <short-name>
  - PR must include: plan, files changed, test results with coverage %, rollback

Exercise: <paste exercise description here>

Create a plan first: list steps and files to change.
Then produce diffs file-by-file.
Include: test strategy, evidence to capture (coverage/contract), and rollback.
Keep scope small and reviewable.
```

---

## Before You Start

1. **Fork & clone** the repo (see [README](../README.md))
2. **Install dependencies:** `python -m pip install pytest pytest-cov`
3. **Run tests:** `cd samples/book-app-project && python -m pytest tests/ -v`
4. **Read the docs:** [CONTRIBUTING.md](../CONTRIBUTING.md) for the full Walk workflow

## Key Docs

| Doc | Purpose |
|---|---|
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Walk workflow and PR process |
| [build-test.md](build-test.md) | How to build and test |
| [pr-conventions.md](pr-conventions.md) | Commit and PR format |
| [SYSTEM-OVERVIEW.md](SYSTEM-OVERVIEW.md) | Architecture overview |
| [security.md](security.md) | Security guidelines |
| [feature-flags.md](feature-flags.md) | Feature flag patterns |
