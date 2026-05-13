# Feature Flags

## `BOOK_APP_CASE_SENSITIVE`

| Setting | Value | Behavior |
|---|---|---|
| Default (OFF) | `0` or unset | Title lookups are case-insensitive (`"dune"` matches `"Dune"`) |
| ON | `1` | Title lookups require exact case (`"Dune"` only) |

### How to Use

```powershell
# Case-insensitive (default)
python book_app.py

# Case-sensitive
$env:BOOK_APP_CASE_SENSITIVE="1"; python book_app.py
```

### Tests

Both modes are tested:
- `test_find_book_case_insensitive_mode_off` — verifies default behavior
- `test_find_book_case_sensitive_mode_on` — verifies exact-case matching

### Affected Operations

`find_book_by_title` is used by `mark_as_read` and `remove_book`, so the toggle affects all title-based lookups.
