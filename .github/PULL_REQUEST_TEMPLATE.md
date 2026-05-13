## Summary

<!-- What changed and why. Keep it to 2-3 sentences. -->

- 

## Review Focus

<!-- Where should the reviewer spend the most time?
     List 2-4 specific areas ranked by importance.
     Example:
     - Logic change in books.py add_book — new validation rules
     - Test coverage for edge cases in test_books.py
     - Schema change in golden file — intentional, see commit message
-->

1. 
2. 

## Files Changed

<!-- List key files touched and what changed in each. -->

| File | Change |
|---|---|
|  |  |

## Evidence

<!-- Paste test output, coverage %, lint results, or screenshots. -->

```
<paste test/coverage output here>
```

## Verification Steps

<!-- Step-by-step instructions for a reviewer to verify locally.
     Be specific: include exact commands and expected output. -->

1. `git checkout <branch>`
2. `cd samples/book-app-project`
3. `python -m pytest tests/ -v --cov=. --cov-report=term-missing`
4. `python -m ruff check .`
5. Expected: all tests pass, lint clean, coverage ≥ ___%

## Risk & Rollback

- **Risk:** low / medium / high
- **What could go wrong:** <!-- e.g., "breaks serialization if golden file not updated" -->
- **Rollback:** `git revert <SHA>` — no data migration needed
- **Monitoring:** <!-- e.g., "check logs for op=save_books status=error" -->

## Reviewer Checklist

<!-- The reviewer should check these before approving. -->

- [ ] Tests pass locally
- [ ] Coverage maintained or improved
- [ ] No new lint/security warnings
- [ ] Documentation updated if behavior changed
- [ ] Commit message follows `<level>: ex<N> <short-name>` convention

## Track

- **Level:** Crawl / Walk / Run
- **Exercise:** Ex _
