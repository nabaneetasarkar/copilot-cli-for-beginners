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

## Improvement 2: Generic `retry_with_backoff` Helper (Run Ex 15)

### Problem
Retry logic was inline in `save_books`, making it hard to reuse for other call paths and difficult to maintain consistently.

### Solution
Extracted a **reusable `retry_with_backoff` function** at the module level:

```python
def retry_with_backoff(fn, *, max_retries=3, backoff_base=0.1,
                       op="unknown", exceptions=(OSError,)):
```

| Parameter | Purpose |
|---|---|
| `fn` | Zero-argument callable to execute |
| `max_retries` | Total number of attempts |
| `backoff_base` | Initial delay in seconds (doubles each retry) |
| `op` | Operation name for structured log messages |
| `exceptions` | Tuple of exception types to catch and retry |

### Applied To

| Call Path | Exceptions Caught | Constants |
|---|---|---|
| `save_books` (atomic write) | `OSError` | `SAVE_MAX_RETRIES=3`, `SAVE_BACKOFF_BASE=0.1` |
| `load_books` (file read) | `PermissionError` | `LOAD_MAX_RETRIES=2`, `LOAD_BACKOFF_BASE=0.05` |

### Tuning Guide

| Constant | Default | Effect |
|---|---|---|
| `SAVE_MAX_RETRIES` | 3 | Number of save attempts before giving up |
| `SAVE_BACKOFF_BASE` | 0.1s | First retry delay for saves (doubles each attempt) |
| `LOAD_MAX_RETRIES` | 2 | Number of load attempts on PermissionError |
| `LOAD_BACKOFF_BASE` | 0.05s | First retry delay for loads |

- **Total worst-case save wait:** 0.3s (0.1 + 0.2)
- **Total worst-case load wait:** 0.05s
- For typical antivirus/lock scenarios, the defaults are sufficient
- Tests monkeypatch all constants to 0 for speed

### Rollback

To revert to inline retry behavior:
1. Delete the `retry_with_backoff` function
2. Restore the inline retry loop in `save_books` (git diff the commit)
3. Remove the `_load_books_inner` method and flatten `load_books`
4. Drop `LOAD_MAX_RETRIES` and `LOAD_BACKOFF_BASE` constants

---

## Failure Tests

| Test | What It Proves |
|---|---|
| `test_save_books_survives_corrupt_load` | Corrupt JSON file doesn't crash — collection starts empty and can still save |
| `test_save_books_atomic_write_on_disk_error` | All retries exhausted → `OSError` raised |
| `test_save_books_retry_succeeds_after_transient_failure` | First attempt fails, retry succeeds — book is saved correctly |
| `test_retry_with_backoff_succeeds_after_failures` | Generic helper recovers on third attempt |
| `test_retry_with_backoff_exhausts_retries` | Generic helper raises last exception after exhaustion |
| `test_retry_with_backoff_custom_exceptions` | Helper only catches specified exception types |
| `test_load_books_retries_permission_error` | `load_books` retries on file-locked PermissionError |
| `test_load_books_permission_error_exhausted` | `load_books` raises after retry exhaustion |

## Key Behavior
- **Happy path:** Single call, no retry overhead
- **Transient failure:** Retries with exponential backoff, logs each attempt at WARNING level
- **Retry success:** Logged at INFO level with attempt number
- **Permanent failure:** Original exception re-raised after all retries, logged at ERROR level
- **Crash during write:** Original file preserved (temp file is discarded)
