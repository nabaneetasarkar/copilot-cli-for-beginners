# Feature Flags

## Flag Lifecycle (Walk Ex 13)

Every feature flag follows this lifecycle:

```
1. INTRODUCE  →  Add flag (default OFF), implement gated behavior
2. TEST       →  Add tests for both ON and OFF states
3. VALIDATE   →  Run tests with flag ON and OFF locally or in CI
4. PROMOTE    →  Once stable, decide: make default ON, or remove flag
5. RETIRE     →  Remove flag, hardcode the chosen behavior, update docs
```

### Rules

- Flags default to **OFF** (opt-in behavior)
- Every flag must have tests for **both states**
- Flag reads happen at **module load time** (env var checked once)
- Document each flag in this file with: name, values, behavior, affected operations

---

## Active Flags

### `BOOK_APP_CASE_SENSITIVE`

| Setting | Value | Behavior |
|---|---|---|
| Default (OFF) | `0` or unset | Title lookups are case-insensitive (`"dune"` matches `"Dune"`) |
| ON | `1` | Title lookups require exact case (`"Dune"` only) |

**Lifecycle stage:** Validate — tested ON/OFF, stable

**How to Use:**

```powershell
# Case-insensitive (default)
python book_app.py

# Case-sensitive
$env:BOOK_APP_CASE_SENSITIVE="1"; python book_app.py
```

**Tests:**
- `test_find_book_case_insensitive_mode_off` — verifies default behavior
- `test_find_book_case_sensitive_mode_on` — verifies exact-case matching

**Affected operations:** `find_book_by_title`, `mark_as_read`, `remove_book`

---

### `BOOK_APP_STRICT_VALIDATION`

| Setting | Value | Behavior |
|---|---|---|
| Default (OFF) | `0` or unset | Duplicate titles are allowed |
| ON | `1` | `add_book` rejects duplicate titles (case-insensitive) with `ValueError` |

**Lifecycle stage:** Validate — tested ON/OFF, candidate for promotion

**How to Use:**

```powershell
# Allow duplicates (default)
python book_app.py

# Reject duplicates
$env:BOOK_APP_STRICT_VALIDATION="1"; python book_app.py
```

**Tests:**
- `test_strict_validation_off_allows_duplicates` — verifies duplicates allowed when OFF
- `test_strict_validation_on_rejects_duplicates` — verifies rejection when ON
- `test_strict_validation_on_case_insensitive` — verifies case-insensitive duplicate check

**Affected operations:** `add_book`

---

## Validation Evidence (Walk Ex 13)

Both flags tested with ON and OFF states:

```
tests/test_books.py::test_find_book_case_insensitive_mode_off PASSED
tests/test_books.py::test_find_book_case_sensitive_mode_on PASSED
tests/test_books.py::test_strict_validation_off_allows_duplicates PASSED
tests/test_books.py::test_strict_validation_on_rejects_duplicates PASSED
tests/test_books.py::test_strict_validation_on_case_insensitive PASSED
```
