# Backlog — System-Level Improvements (Run Ex 12)

Epic: **Book App Subsystem — Production Hardening Phase 2**

Generated from AI review (Ex 11), observability sweep (Ex 9), CI reliability (Ex 10), and security sweep (Ex 8) findings. Scoped to `samples/book-app-project/`.

---

## Status Key

- [ ] Not started
- [x] Completed

---

## 1. Add `find_book_by_title` structured logging

**Priority:** Low | **Effort:** Small

**Why:** All public `BookCollection` methods emit structured logs except `find_book_by_title`. Identified as finding L3 in [ai-review.md](ai-review.md). Inconsistent instrumentation makes it harder to trace lookup operations end-to-end.

**Code:** [`books.py` — `find_book_by_title`](../samples/book-app-project/books.py) (lines 195–207)

**Acceptance Criteria:**
- [ ] `find_book_by_title` emits a structured log with `op`, `status` (`ok`/`not_found`), `title`
- [ ] Log respects both `CASE_SENSITIVE` mode paths
- [ ] Existing tests still pass
- [ ] `logging.md` updated

---

## 2. CLI integration tests via subprocess

**Priority:** Medium | **Effort:** Medium

**Why:** `book_app.py` has 0% test coverage (finding M3 in [ai-review.md](ai-review.md)). The CLI handlers are the only untested code path. Subprocess-based tests avoid mocking `input()` and verify the real entry point.

**Code:** [`book_app.py`](../samples/book-app-project/book_app.py), [`tests/`](../samples/book-app-project/tests/)

**Acceptance Criteria:**
- [ ] Test: `python book_app.py` (no args) exits 0 and prints help
- [ ] Test: `python book_app.py list` with empty collection prints "No books found"
- [ ] Test: `python book_app.py badcommand` prints "Unknown command"
- [ ] `book_app.py` coverage ≥ 40%
- [ ] Tests use `tmp_path` for isolated data file

---

## 3. Configurable `DATA_FILE` path via environment variable

**Priority:** Medium | **Effort:** Small

**Why:** `DATA_FILE` is a hardcoded relative path (`"data.json"`), making behavior CWD-dependent (finding M1 in [ai-review.md](ai-review.md)). An env var override would allow deployment flexibility without code changes.

**Code:** [`books.py` — line 10](../samples/book-app-project/books.py)

**Acceptance Criteria:**
- [ ] `DATA_FILE` reads from `BOOK_APP_DATA_FILE` env var, defaulting to `"data.json"`
- [ ] Test: setting `BOOK_APP_DATA_FILE` changes the file path
- [ ] Existing tests still pass (they already monkeypatch `DATA_FILE`)
- [ ] `feature-flags.md` updated with the new env var
- [ ] Rollback: unset env var → original behavior

---

## 4. Add `--json` output mode to CLI

**Priority:** Low | **Effort:** Medium

**Why:** All internal operations use structured JSON logging, but CLI output is human-readable only. A `--json` flag would enable scripting and piping (e.g., `book_app.py list --json | jq`).

**Code:** [`book_app.py` — `handle_list`, `handle_find`](../samples/book-app-project/book_app.py), [`utils.py` — `format_book_list`](../samples/book-app-project/utils.py)

**Acceptance Criteria:**
- [ ] `python book_app.py list --json` outputs JSON array of book objects
- [ ] `python book_app.py find --json` outputs JSON array of matching books
- [ ] Default (no flag) behavior unchanged
- [ ] Test: JSON output is valid and matches book schema
- [ ] Flag documented in `show_help()`

---

## 5. Type-safe `stats()` return with TypedDict

**Priority:** Low | **Effort:** Small

**Why:** `stats()` returns `dict` — callers have no type safety on keys or value types (finding L2 in [ai-review.md](ai-review.md)). A `TypedDict` makes the contract explicit at the type level, complementing the existing contract tests.

**Code:** [`books.py` — `stats`](../samples/book-app-project/books.py) (lines 261–273)

**Acceptance Criteria:**
- [ ] `StatsResult = TypedDict("StatsResult", ...)` defined
- [ ] `stats()` return type annotated as `StatsResult`
- [ ] Existing `test_stats_contract_*` tests still pass
- [ ] `mypy --strict` passes on `books.py` (or ruff type-checking equivalent)

---

## Cross-References

| Item | Source Finding | AI Review Ref |
|---|---|---|
| 1 | Observability gap | L3 |
| 2 | Coverage gap | M3 |
| 3 | CWD dependency | M1 |
| 4 | CLI extensibility | New (from observability sweep) |
| 5 | Type safety | L2 |
