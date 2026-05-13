# Resilience — Ex 15

## Improvement: Atomic Write for `save_books`

### Problem
`save_books` previously wrote directly to `data.json`. If the process crashed or disk filled up mid-write, the file could be left half-written and corrupted — losing all book data.

### Solution
Replaced direct write with **atomic write**:
1. Serialize data to a temp file (`.books_*.tmp`) in the same directory
2. `os.replace()` the temp file over `data.json` (atomic on all OSes)
3. If any step fails, the temp file is cleaned up and `IOError` is raised — the original `data.json` is never touched

### Failure Tests

| Test | What It Proves |
|---|---|
| `test_save_books_survives_corrupt_load` | Corrupt JSON file doesn't crash the app — collection starts empty and can still save |
| `test_save_books_atomic_write_on_disk_error` | Disk failure (simulated via mocked `mkstemp`) raises `IOError` with clear message |

### Key Behavior
- **Happy path:** Identical to before — books saved to `data.json`
- **Crash during write:** Original file preserved (temp file is discarded)
- **Disk error:** `IOError` raised, logged at ERROR level, original file untouched
