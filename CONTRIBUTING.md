# Contributing

Hi there! We're thrilled that you'd like to contribute to this project. Your help is essential for keeping it great.

Contributions to this project are [released](https://help.github.com/articles/github-terms-of-service/#6-contributions-under-repository-license) to the public under the [project's open source license](LICENSE).

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

---

## Walk Workflow

This project follows the **Crawl → Walk → Run** AI Engineering Track. Contributors working through the Walk track should follow this workflow for every exercise:

### 1. Branch

Create a feature branch from the previous exercise branch (chained) or from `main` (isolated):

```
git checkout -b walk/<github-id>/ex<N>-<short-name>
```

### 2. Plan First

Before writing any code, create a plan:

- List the files you will change (2–4 files typical)
- Describe what changes each file needs
- Identify the test strategy (new tests, updated tests, coverage target)
- Note any risks or rollback steps

Use this prompt with GitHub Copilot Chat:

```
Create a plan first: list steps and files to change.
Then produce diffs file-by-file.
Include: test strategy, evidence to capture (coverage/contract), and rollback.
Keep scope small and reviewable.
```

### 3. Implement

- Make changes file-by-file, following your plan
- Run tests after each file change to catch regressions early
- Keep changes small and focused on the exercise goal

### 4. Verify

```powershell
cd samples/book-app-project
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

- All tests must pass
- Include coverage % in your PR description

### 5. Commit & PR

Follow [PR & commit conventions](ai-track-docs/pr-conventions.md):

```
walk: ex<N> <short-name>
```

Every PR description should include: Summary, Files Changed, Test Results (with coverage %), and Risk/Rollback notes.

### 6. Review

- Link your PR for review
- Include verification steps so reviewers can reproduce locally

---

## Quick Reference

| Resource | Location |
|---|---|
| Build & Test | [ai-track-docs/build-test.md](ai-track-docs/build-test.md) |
| PR Conventions | [ai-track-docs/pr-conventions.md](ai-track-docs/pr-conventions.md) |
| Architecture | [ai-track-docs/SYSTEM-OVERVIEW.md](ai-track-docs/SYSTEM-OVERVIEW.md) |
| Security | [ai-track-docs/security.md](ai-track-docs/security.md) |
| Onboarding Prompt | [ai-track-docs/onboarding-prompt.md](ai-track-docs/onboarding-prompt.md) |
