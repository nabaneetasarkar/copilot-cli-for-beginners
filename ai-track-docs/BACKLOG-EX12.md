# Backlog — Ex 12

Items generated from repo observations during Crawl exercises 0–11.

---

## 1. Add duplicate-title prevention to `add_book`

**Why:** Currently `add_book` allows adding multiple books with the same title. This creates ambiguity for `find_book_by_title`, `mark_as_read`, and `remove_book` — all of which match on title.

**Code:** [`samples/book-app-project/books.py` — `add_book`](../samples/book-app-project/books.py)

**Acceptance Criteria:**
- [ ] `add_book` raises `ValueError` if a book with the same title already exists (case-insensitive)
- [ ] Test added: calling `add_book` twice with the same title raises
- [ ] Existing tests still pass

---

## 2. Add test coverage for `find_by_author`

**Why:** `find_by_author` has no tests. It's the only public method on `BookCollection` without coverage.

**Code:** [`samples/book-app-project/books.py` — `find_by_author`](../samples/book-app-project/books.py), [`samples/book-app-project/tests/test_books.py`](../samples/book-app-project/tests/test_books.py)

**Acceptance Criteria:**
- [ ] Test: finding by author returns correct books (case-insensitive)
- [ ] Test: finding by non-existent author returns empty list
- [ ] Test: multiple books by same author all returned

---

## 3. Handle `book_app.py` CLI input errors gracefully

**Why:** `handle_add()` in `book_app.py` catches `ValueError` from `add_book`, but `handle_remove()` and `handle_find()` have no error handling. If `BookCollection` methods raise in the future, the CLI will crash with a traceback.

**Code:** [`samples/book-app-project/book_app.py` — `handle_remove`, `handle_find`](../samples/book-app-project/book_app.py)

**Acceptance Criteria:**
- [ ] `handle_remove` and `handle_find` wrapped in try/except with user-friendly error messages
- [ ] No traceback shown to the user on bad input
- [ ] Manual smoke test documented

---

## 4. Add structured logging to `mark_as_read`

**Why:** In Ex 9, structured logs were added to `load_books`, `add_book`, and `remove_book` — but `mark_as_read` was missed. It's a mutation operation that should also be logged for consistency.

**Code:** [`samples/book-app-project/books.py` — `mark_as_read`](../samples/book-app-project/books.py)

**Acceptance Criteria:**
- [ ] `mark_as_read` emits structured JSON log with `op`, `status` (ok/not_found), `title`, `elapsed_ms`
- [ ] Log format matches existing pattern from Ex 9
- [ ] Existing tests still pass

---

## 5. Add `--verbose` flag to `validate.py`

**Why:** The validation script prints all test output by default. For quick checks, a summary-only mode would be useful. Conversely, a `--verbose` flag could show timing per check.

**Code:** [`validate.py`](../validate.py)

**Acceptance Criteria:**
- [ ] Default mode: show pass/fail summary only (suppress pytest verbose output)
- [ ] `--verbose` flag: show full pytest output (current behavior)
- [ ] Exit code behavior unchanged (0 = pass, 1 = fail)
