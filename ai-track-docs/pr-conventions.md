# PR & Commit Conventions

## Commit Message Format

```
<level>: ex<N> <short-name>
```

Examples:
- `crawl: ex0 bootstrap`
- `crawl: ex5 validation`
- `walk: ex3 plan-first-refactor`

### Rules
- Lowercase level prefix (`crawl`, `walk`, `run`)
- Exercise number and short name after the colon
- Keep the first line under 72 characters
- Use imperative mood for any additional detail in the body

## PR Description

Every PR should include these sections (auto-populated by the PR template):

| Section | Purpose |
|---|---|
| **Summary** | What changed and why (2-3 sentences) |
| **Review Focus** | Where the reviewer should spend time |
| **Files Changed** | Key files and what changed |
| **Evidence** | Test output, logs, or metrics proving the change works |
| **Verification Steps** | How to verify locally |
| **Risk & Rollback** | Risk level + how to revert |
| **Reviewer Checklist** | Pre-approval checks for the reviewer |
| **Track** | Level and exercise number |

## Writing Effective Review Focus (Walk Ex 11)

The **Review Focus** section tells the reviewer where to spend time. Good focus bullets:

### Do

- **Be specific about files and functions:** "Logic change in `books.py` `add_book` — new year validation"
- **Rank by importance:** put the riskiest change first
- **Call out intentional changes:** "Golden file updated — schema change is intentional"
- **Flag areas of uncertainty:** "Not sure if `_rebuild_index` handles duplicates correctly"

### Don't

- Don't say "please review everything" — that's the same as saying nothing
- Don't list trivial changes (whitespace, imports) — reviewers can see those
- Don't repeat the summary — focus tells *where* to look, summary tells *what* changed

### Examples

**Good:**
1. New validation in `books.py` `add_book` — rejects years > current year
2. Edge case test for year 0 in `test_books.py` — boundary behavior
3. Golden file updated to match new field default

**Bad:**
- Updated some files
- Please check my code
- Made changes to books.py

## Verification Steps Guide

Verification steps should be **copy-paste ready**. A reviewer should be able to run them without thinking:

```markdown
1. `git checkout walk/user/ex11-pr-review-focus`
2. `cd samples/book-app-project`
3. `python -m pytest tests/ -v --cov=. --cov-report=term-missing`
4. `python -m ruff check .`
5. Expected: 18 tests pass, coverage ≥ 68%, lint clean
```

## Rollback Guide

Every PR should answer: "If this breaks production, how do I undo it?"

| Scenario | Rollback |
|---|---|
| Code-only change | `git revert <SHA>` |
| Schema/data change | Revert + re-run migration or update golden file |
| Config change | Revert the config file, redeploy |
| Dependency change | `git revert <SHA>`, then `pip install -e ".[dev]"` |

## Past Commit Messages — Review

| Commit | Current | Suggested Improvement |
|---|---|---|
| Ex 0 | `crawl: ex0 bootstrap` | Good — follows convention |
| Ex 1 | `crawl: ex1 repo-orientation` | Good |
| Ex 2 | `crawl: ex2 build-test-baseline` | Good |
| Ex 3 | `crawl: ex3 tiny-refactor` | Good |
| Ex 4 | `crawl: ex4 doc-sync` | Good |
| Ex 5 | `crawl: ex5 validation` | Good |
| Ex 6 | `crawl: ex6 perf-baseline` | Good |
| Ex 7 | `crawl: ex7 dep-hygiene` | Good |
| Ex 8 | `crawl: ex8 security` | Good |
| Ex 9 | `crawl: ex9 logging` | Good |
| Ex 10 | `crawl: ex10 ci-baseline` | Good |

All commit messages follow the convention consistently. No changes needed.
