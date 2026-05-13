# AI Review — Book App Subsystem

## Review Scope

| File | Lines | Coverage | Layer |
|---|---|---|---|
| books.py | 147 | 95% | Data |
| book_app.py | 59 | 0% | CLI |
| utils.py | 38 | 50% | Input |
| tests/test_books.py | 234 | 100% | Tests |

## Risk Assessment

### HIGH — No risks identified

No high-severity issues found. The subsystem uses no network calls, no user authentication, no database, and no third-party runtime dependencies.

### MEDIUM

| # | Finding | Status | Response |
|---|---|---|---|
| M1 | `DATA_FILE` is a module-level relative path — behavior depends on CWD | Accepted | Intentional for a CLI app; documented in extending-books.md |
| M2 | `CASE_SENSITIVE` and `STRICT_VALIDATION` are read once at import time — cannot toggle at runtime | Accepted | By design for safety; documented in feature-flags.md |
| M3 | `book_app.py` has 0% test coverage | Accepted | CLI entry point with `input()` calls; testing would require extensive mocking. Handlers delegate to tested `BookCollection` methods |

### LOW

| # | Finding | Status | Response |
|---|---|---|---|
| L1 | `load_books` uses `print()` for user warnings (corrupt file, oversized file) alongside `logger.warning` | Accepted | CLI app — users need visible console output; structured logs for operators |
| L2 | No type annotation on `stats()` return (`dict` not `dict[str, int]`) | Accepted | Contract tested via `test_stats_contract_types`; adding precise typing is low value |
| L3 | `find_book_by_title` doesn't log (unlike other operations) | Noted | Low impact — called internally by `mark_as_read` and `remove_book`, which do log |

## Verification Matrix

| Behavior | Test | Passing |
|---|---|---|
| Add book (valid) | `test_add_book` | Yes |
| Add book (empty title) | `test_add_book_empty_title_raises` | Yes |
| Add book (empty author) | `test_add_book_empty_author_raises` | Yes |
| Add book (negative year) | `test_add_book_negative_year_raises` | Yes |
| Add book (year > MAX_YEAR) | `test_year_upper_bound_rejected` | Yes |
| Add book (year == MAX_YEAR) | `test_year_at_max_accepted` | Yes |
| Mark as read (valid) | `test_mark_book_as_read` | Yes |
| Mark as read (not found) | `test_mark_book_as_read_invalid` | Yes |
| Remove book (valid) | `test_remove_book` | Yes |
| Remove book (not found) | `test_remove_book_invalid` | Yes |
| Find by title (case-insensitive) | `test_find_book_by_title_case_insensitive` | Yes |
| Find by title (case-sensitive mode) | `test_find_book_case_sensitive_mode_on` | Yes |
| STRICT_VALIDATION on (rejects dupes) | `test_strict_validation_on_rejects_duplicates` | Yes |
| STRICT_VALIDATION on (case-insensitive) | `test_strict_validation_on_case_insensitive` | Yes |
| STRICT_VALIDATION off (allows dupes) | `test_strict_validation_off_allows_duplicates` | Yes |
| Corrupt data.json recovery | `test_save_books_survives_corrupt_load` | Yes |
| Atomic write disk error (retry exhaustion) | `test_save_books_atomic_write_on_disk_error` | Yes |
| Retry succeeds after transient failure | `test_save_books_retry_succeeds_after_transient_failure` | Yes |
| Oversized data.json rejected | `test_load_rejects_oversized_file` | Yes |
| Unknown JSON keys stripped | `test_load_strips_unknown_keys` | Yes |
| Golden file save roundtrip | `test_save_produces_golden_json` | Yes |
| Golden file load roundtrip | `test_load_roundtrip_from_golden` | Yes |
| Golden schema keys | `test_golden_schema_keys` | Yes |
| stats() contract keys | `test_stats_contract_keys` | Yes |
| stats() contract types | `test_stats_contract_types` | Yes |
| stats() contract values | `test_stats_contract_values` | Yes |
| Display format contract | `test_format_book_list_contract_line_pattern` | Yes |
| format_book_list (empty) | `test_format_book_list_empty` | Yes |
| format_book_list (with books) | `test_format_book_list_with_books` | Yes |
| get_title_input whitespace | `test_get_title_input_strips_whitespace` | Yes |
| get_author_input whitespace | `test_get_author_input_strips_whitespace` | Yes |

## Edge Cases Reviewed

| Edge Case | Covered | How |
|---|---|---|
| Empty data.json `[]` | Yes | Default test fixture |
| Missing data.json | Yes | `FileNotFoundError` path in `load_books` |
| Corrupted data.json | Yes | `test_save_books_survives_corrupt_load` |
| Oversized data.json (>10 MB) | Yes | `test_load_rejects_oversized_file` |
| Unknown keys in JSON records | Yes | `test_load_strips_unknown_keys` |
| Concurrent writes | Documented | Atomic write via `tempfile.mkstemp` + `os.replace` |
| Disk full during save | Yes | `test_save_books_atomic_write_on_disk_error` |
| Year = 0 | Yes | Passes validation (0 is valid) |
| Year = -1 | Yes | `test_add_book_negative_year_raises` |
| Year = 10000 | Yes | `test_year_upper_bound_rejected` |
| Whitespace-only title | Yes | `test_add_book_empty_title_raises` |
| Case-insensitive duplicate title | Yes | `test_strict_validation_on_case_insensitive` |

## Recommendations for Future PRs

1. Add `find_book_by_title` logging (low priority — L3 above)
2. Consider integration tests for `book_app.py` CLI handlers via subprocess
3. Add `typing.TypedDict` for `stats()` return type if API grows

## How to Use This Review

When creating a PR for the book-app subsystem:

1. Copy the **AI Review** section from the PR template
2. Use Copilot to fill in risks, verification matrix, and edge cases
3. Cross-reference this doc for known accepted risks (avoid re-litigating M1-M3, L1-L3)
4. Add new findings to this doc as they are discovered
