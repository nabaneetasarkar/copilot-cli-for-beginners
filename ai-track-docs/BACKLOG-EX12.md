# Backlog — Book App Improvements

Epic: **Harden book-app-project for production readiness**

Items generated from observations during Crawl (Ex 0–15) and Walk (Ex 1–11) exercises.

---

## Status Key

- [ ] Not started
- [x] Completed

---

## 1. Add duplicate-title prevention to `add_book`

**Why:** `add_book` allows multiple books with the same title. With the `_title_index` (Walk Ex 6), the last-added book silently overwrites the index entry, making earlier duplicates unfindable.

**Code:** [`samples/book-app-project/books.py` — `add_book`](../samples/book-app-project/books.py)

**Acceptance Criteria:**
- [ ] `add_book` raises `ValueError` if a book with the same title already exists (case-insensitive check via `_title_index`)
- [ ] Test added: calling `add_book` twice with the same title raises
- [ ] Existing tests still pass
- [ ] Golden file unaffected (no schema change)

---

## 2. Add test coverage for `find_by_author` and `stats()`

**Why:** `find_by_author` (original) and `stats()` (Walk Ex 9) have no direct tests. Coverage gaps: `books.py` lines 178–197.

**Code:** [`samples/book-app-project/books.py`](../samples/book-app-project/books.py), [`samples/book-app-project/tests/test_books.py`](../samples/book-app-project/tests/test_books.py)

**Acceptance Criteria:**
- [ ] Test: `find_by_author` returns correct books (case-insensitive)
- [ ] Test: `find_by_author` with non-existent author returns empty list
- [ ] Test: `stats()` returns correct total/read/unread/unique_authors counts
- [ ] Coverage for `books.py` reaches ≥ 97%

---

## 3. Handle CLI input errors gracefully in `book_app.py`

**Why:** `handle_add()` catches `ValueError`, but `handle_remove()` and `handle_find()` have no error handling. Future validation in `BookCollection` methods would cause CLI tracebacks.

**Code:** [`samples/book-app-project/book_app.py` — `handle_remove`, `handle_find`](../samples/book-app-project/book_app.py)

**Acceptance Criteria:**
- [ ] `handle_remove` and `handle_find` wrapped in try/except with user-friendly messages
- [ ] No traceback shown to end users
- [ ] Manual smoke test documented in PR

---

## 4. Add `--verbose` flag to `validate.py`

**Why:** The validation script prints all test output by default. For quick CI checks, summary-only mode would reduce noise.

**Code:** [`validate.py`](../validate.py)

**Acceptance Criteria:**
- [ ] Default mode: show pass/fail summary only
- [ ] `--verbose` flag: show full pytest/ruff output
- [ ] Exit code unchanged (0 = pass, 1 = fail)

---

## 5. CLI integration tests for `book_app.py`

**Why:** `book_app.py` has 0% coverage. All handlers (`handle_list`, `handle_add`, `handle_remove`, `handle_find`) are untested. The CI soft gate (Walk Ex 10) would catch regressions if tests existed.

**Code:** [`samples/book-app-project/book_app.py`](../samples/book-app-project/book_app.py), [`samples/book-app-project/tests/`](../samples/book-app-project/tests/)

**Acceptance Criteria:**
- [ ] Test: `main()` with no args shows help
- [ ] Test: `handle_list` with empty and populated collection
- [ ] Test: `handle_add` with valid and invalid input (mocked stdin)
- [ ] `book_app.py` coverage ≥ 50%
- [ ] Overall project coverage ≥ 75%

---

## Completed Items

### ~~Add structured logging to `mark_as_read`~~
- [x] Completed in Walk Ex 9 — `mark_as_read` now emits structured JSON log with op/status/title

---

## Priority Order

| Priority | Item | Effort | Impact |
|---|---|---|---|
| P1 | #1 Duplicate prevention | Small | Prevents data corruption |
| P1 | #2 Test coverage gaps | Small | Improves confidence |
| P2 | #5 CLI integration tests | Medium | Covers 0% → 50%+ |
| P2 | #3 CLI error handling | Small | User experience |
| P3 | #4 Verbose flag | Small | Developer convenience |
