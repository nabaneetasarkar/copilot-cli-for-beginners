# Evidence Capture Guide

Standard patterns for capturing and presenting evidence in PRs. Every PR should include at least one concrete artifact proving the change works.

---

## Evidence Types

| Type | When to use | How to capture |
|---|---|---|
| **Test output** | Every PR with code changes | `pytest -v --cov` output |
| **Lint output** | Every PR with code changes | `ruff check .` output |
| **Before/after metrics** | Performance changes | Benchmark script output |
| **Log samples** | Observability changes | Structured log JSON snippets |
| **Security scan** | Security-related changes | `bandit` output |
| **CI summary** | CI changes | Link to workflow run or job summary |

---

## Capture Commands

Run these from `samples/book-app-project/`:

### Tests + Coverage

```powershell
python -m pytest tests/ -v --cov=. --cov-report=term-missing 2>&1 | Tee-Object -FilePath evidence-tests.txt
```

### Lint

```powershell
python -m ruff check . 2>&1 | Tee-Object -FilePath evidence-lint.txt
```

### Security Scan

```powershell
python -m bandit -r . -x ./tests 2>&1 | Tee-Object -FilePath evidence-security.txt
```

### Benchmark (if applicable)

```powershell
python bench_find.py 2>&1 | Tee-Object -FilePath evidence-bench.txt
```

> **Tip:** `Tee-Object` prints to the terminal AND saves to a file. Don't commit evidence files — they're for pasting into the PR.

---

## PR Evidence Section Template

Paste this into the `## Evidence` section of your PR:

```markdown
## Evidence

### Tests
<count> tests pass, coverage <percent>%

```
<paste last few lines of pytest output here>
```

### Lint
```
All checks passed!
```

### Additional Evidence
<paste benchmark output, log samples, scan results as applicable>
```

---

## Evidence by Change Type

### Code changes (features, fixes, refactors)

Required:
- [ ] Test output with pass count and coverage %
- [ ] Lint output (clean)

### Performance changes

Required:
- [ ] Before/after benchmark output with numbers
- [ ] Test output (no regressions)

### Security changes

Required:
- [ ] Security scan output (bandit)
- [ ] Test output (no regressions)

### Documentation-only changes

Required:
- [ ] State "documentation only — no code changes"
- [ ] Confirm no test regressions if docs reference tested behavior

### CI/workflow changes

Required:
- [ ] Link to successful workflow run
- [ ] Job summary screenshot or paste

---

## Anti-Patterns

| Don't | Do instead |
|---|---|
| "Tests pass" with no output | Paste actual pytest output |
| Screenshot of terminal | Copy-paste text (searchable, accessible) |
| Evidence from a different branch | Re-run on the PR branch |
| Skip evidence for "trivial" changes | At minimum: test count + lint status |
| Commit evidence files to repo | Paste into PR description, delete local files |

---

## Quick Reference

Minimum evidence for any code PR:

```
## Evidence

22/22 tests pass, coverage 72%
ruff check: All checks passed
```

This takes ~5 seconds to capture and dramatically improves review confidence.
