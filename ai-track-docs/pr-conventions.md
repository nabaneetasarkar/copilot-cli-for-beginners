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
| **Track** | Level and exercise number |

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
