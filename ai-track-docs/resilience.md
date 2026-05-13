# Resilience

## Improvement 1: Atomic Write for `save_books` (Crawl Ex 15)

### Problem
`save_books` previously wrote directly to `data.json`. If the process crashed or disk filled up mid-write, the file could be left half-written and corrupted — losing all book data.

### Solution
Replaced direct write with **atomic write**:
1. Serialize data to a temp file (`.books_*.tmp`) in the same directory
2. `os.replace()` the temp file over `data.json` (atomic on all OSes)
3. If any step fails, the temp file is cleaned up and `OSError` is raised — the original `data.json` is never touched

---

## Improvement 2: Retry with Exponential Backoff (Walk Ex 15)

### Problem
Transient disk errors (antivirus locks, momentary I/O contention) cause `save_books` to fail permanently, even when the issue resolves within milliseconds.

### Solution
Wrapped the atomic write in a **retry loop** with exponential backoff:

| Parameter | Default | Env override |
|---|---|---|
| `SAVE_MAX_RETRIES` | 3 | Hardcoded constant |
| `SAVE_BACKOFF_BASE` | 0.1s | Hardcoded constant |

**Backoff schedule:** 0.1s → 0.2s → (give up)

```
Attempt 1: try write → fail → sleep 0.1s
Attempt 2: try write → fail → sleep 0.2s
Attempt 3: try write → fail → raise OSError
```

### Tuning
- `SAVE_MAX_RETRIES` and `SAVE_BACKOFF_BASE` are module-level constants in `books.py`
- Tests monkeypatch both to 0 delay for speed
- For production use, 3 retries with 0.1s base covers typical antivirus/lock scenarios
- Total worst-case wait: 0.3s (0.1 + 0.2)

---

## Failure Tests

| Test | What It Proves |
|---|---|
| `test_save_books_survives_corrupt_load` | Corrupt JSON file doesn't crash — collection starts empty and can still save |
| `test_save_books_atomic_write_on_disk_error` | All retries exhausted → `OSError` raised with "after N attempts" message |
| `test_save_books_retry_succeeds_after_transient_failure` | First attempt fails, retry succeeds — book is saved correctly |

## Key Behavior
- **Happy path:** Single write, no retry overhead
- **Transient failure:** Retries with backoff, logs each attempt at WARNING level
- **Retry success:** Logged at INFO level with attempt number
- **Permanent failure:** `OSError` raised after all retries, logged at ERROR level
- **Crash during write:** Original file preserved (temp file is discarded)
