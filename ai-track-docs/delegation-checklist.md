# Delegation Checklist

A repeatable workflow for safely delegating code changes to AI (or any contributor). Every PR produced via delegation should follow these steps.

---

## 1. Patch Plan

Before writing any code, produce a written plan:

- [ ] **Goal** — One sentence describing what changes and why
- [ ] **File scope** — List every file that will be created, modified, or deleted
- [ ] **Out of scope** — Explicitly state what will NOT be touched
- [ ] **Approach** — Brief description of the implementation strategy

### Template

```
Goal: <what and why>
Files:
  - modify: books.py (add retry logic to save_books)
  - modify: tests/test_books.py (add failure tests)
  - modify: ai-track-docs/resilience.md (document behavior)
Out of scope: book_app.py, utils.py, CI workflow
Approach: Wrap atomic write in retry loop with exponential backoff
```

---

## 2. Generate Diffs

- [ ] Implement changes per the patch plan
- [ ] Verify each file in scope was touched — no extras, no omissions
- [ ] Review diffs before committing (use `git diff --stat` then `git diff`)

---

## 3. Tests

- [ ] Run existing tests — confirm no regressions
- [ ] Add or update tests for new behavior
- [ ] Verify coverage meets project baseline (currently 69%+)
- [ ] Run lint (`ruff check .`) — must pass clean

### Commands

```powershell
cd samples/book-app-project
python -m pytest tests/ -v --cov=. --cov-report=term-missing
python -m ruff check .
```

---

## 4. Documentation

- [ ] Update relevant doc in `ai-track-docs/` (or create new one)
- [ ] Docs reference real file paths and function names
- [ ] Include any configuration/tuning guidance

---

## 5. Evidence

Capture concrete proof that the change works:

- [ ] Test output (pass count, coverage %)
- [ ] Lint output (clean or justified suppressions)
- [ ] Before/after metrics (if performance-related)
- [ ] Logs or screenshots (if observability-related)

Evidence goes in the PR description under `## Evidence`.

---

## 6. PR Description

Use the repo's PR template. Ensure these sections are filled:

- [ ] **Summary** — What changed and why
- [ ] **Review Focus** — 3–4 numbered items for the reviewer
- [ ] **Files Changed** — Table mapping files to changes
- [ ] **Evidence** — Test output, lint, metrics
- [ ] **Verification Steps** — Exact commands a reviewer can run
- [ ] **Risk and Rollback** — Risk level + how to revert

---

## 7. Rollback Plan

Every PR must answer: "How do we undo this safely?"

| Scenario | Rollback |
|---|---|
| Code change only | `git revert <commit>` |
| Config change | Restore previous value, re-deploy |
| Feature flag | Set flag to OFF (no code change needed) |
| Dependency upgrade | Pin back to previous version |
| CI change | Revert workflow file |

---

## Pre-Submit Checklist

Before pushing:

```
[ ] Patch plan written and followed
[ ] File scope matches plan (no drift)
[ ] Tests pass (all green, no skips)
[ ] Lint clean (ruff check .)
[ ] Docs updated
[ ] Evidence captured
[ ] PR description complete
[ ] Rollback plan documented
[ ] Commit message follows convention (<level>: <exN> <short-name>)
```

---

## When to Pause and Ask

Stop delegation and consult a human when:

- Change touches shared infrastructure (CI, deploy, config)
- Scope creep — AI suggests changes beyond the plan
- Test failures you don't understand
- Security-sensitive code paths
- Destructive operations (delete, drop, force-push)
