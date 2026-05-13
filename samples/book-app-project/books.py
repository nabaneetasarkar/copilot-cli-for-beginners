from dataclasses import asdict, dataclass
import json
import logging
import os
import tempfile
import time

logger = logging.getLogger(__name__)

DATA_FILE = "data.json"
CASE_SENSITIVE = os.environ.get("BOOK_APP_CASE_SENSITIVE", "0") == "1"
STRICT_VALIDATION = os.environ.get("BOOK_APP_STRICT_VALIDATION", "0") == "1"
SAVE_MAX_RETRIES = 3
SAVE_BACKOFF_BASE = 0.1  # seconds; doubles each retry
MAX_DATA_FILE_BYTES = 10 * 1024 * 1024  # 10 MB — reject oversized data files
MAX_YEAR = 9999
_BOOK_KEYS = frozenset({"title", "author", "year", "read"})


@dataclass
class Book:
    """A single book with title, author, publication year, and read status."""

    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    """Manages a list of Book objects, persisted to a JSON file.

    All mutations (add, remove, mark-as-read) auto-save to disk.
    Lookups by title are case-insensitive.
    """

    def __init__(self):
        self.books: list[Book] = []
        self._title_index: dict[str, Book] = {}
        self._author_index: dict[str, list[Book]] = {}
        self.load_books()

    def _rebuild_index(self):
        """Rebuild title and author lookup indexes in a single pass."""
        title_idx: dict[str, Book] = {}
        author_idx: dict[str, list[Book]] = {}
        for b in self.books:
            title_idx[b.title.lower()] = b
            key = b.author.lower()
            if key not in author_idx:
                author_idx[key] = []
            author_idx[key].append(b)
        self._title_index = title_idx
        self._author_index = author_idx

    def load_books(self):
        """Load books from the JSON file if it exists."""
        start = time.perf_counter()
        try:
            file_size = os.path.getsize(DATA_FILE)
            if file_size > MAX_DATA_FILE_BYTES:
                print(
                    f"Warning: data.json exceeds {MAX_DATA_FILE_BYTES} bytes. "
                    "Refusing to load."
                )
                self.books = []
                logger.warning(json.dumps({
                    "op": "load_books", "status": "file_too_large",
                    "size_bytes": file_size,
                    "limit_bytes": MAX_DATA_FILE_BYTES,
                }))
                return
            with open(DATA_FILE) as f:
                data = json.load(f)
                for record in data:
                    extra = set(record.keys()) - _BOOK_KEYS
                    if extra:
                        logger.warning(json.dumps({
                            "op": "load_books", "status": "unknown_keys",
                            "keys": sorted(extra),
                        }))
                    # Only pass known keys to Book()
                    filtered = {k: record[k] for k in _BOOK_KEYS if k in record}
                    self.books.append(Book(**filtered))
            self._rebuild_index()
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info(json.dumps({
                "op": "load_books", "status": "ok",
                "count": len(self.books),
                "elapsed_ms": round(elapsed_ms, 2),
            }))
        except FileNotFoundError:
            self.books = []
            logger.info(json.dumps({
                "op": "load_books", "status": "no_file",
                "count": 0,
            }))
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []
            logger.warning(json.dumps({
                "op": "load_books", "status": "corrupt_file",
                "count": 0,
            }))

    def save_books(self):
        """Save the current book collection to JSON.

        Uses atomic write (temp file + rename) so a crash or disk error
        never leaves a half-written data file.  Retries up to
        SAVE_MAX_RETRIES times with exponential backoff on transient
        OSError.  If all attempts fail, the original file is preserved
        and an OSError is raised.
        """
        data = json.dumps([asdict(b) for b in self.books], indent=2)
        dir_name = os.path.dirname(os.path.abspath(DATA_FILE))
        last_exc: OSError | None = None

        for attempt in range(1, SAVE_MAX_RETRIES + 1):
            tmp_path = None
            try:
                fd, tmp_path = tempfile.mkstemp(
                    dir=dir_name, suffix=".tmp", prefix=".books_"
                )
                with os.fdopen(fd, "w") as f:
                    f.write(data)
                os.replace(tmp_path, DATA_FILE)
                if attempt > 1:
                    logger.info(json.dumps({
                        "op": "save_books", "status": "ok_after_retry",
                        "attempt": attempt,
                    }))
                return  # success
            except OSError as exc:
                last_exc = exc
                # Clean up temp file if it was created
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                logger.warning(json.dumps({
                    "op": "save_books", "status": "retry",
                    "attempt": attempt,
                    "error": str(exc),
                }))
                if attempt < SAVE_MAX_RETRIES:
                    time.sleep(SAVE_BACKOFF_BASE * (2 ** (attempt - 1)))

        # All retries exhausted
        logger.error(json.dumps({
            "op": "save_books", "status": "error",
            "error": str(last_exc),
        }))
        raise OSError(
            f"Failed to save books after {SAVE_MAX_RETRIES} attempts: "
            f"{last_exc}"
        ) from last_exc

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Create a new Book, append it to the collection, and save.

        Raises:
            ValueError: If title or author is empty, or year is negative.
        """
        if not title or not title.strip():
            raise ValueError("Title must not be empty.")
        if not author or not author.strip():
            raise ValueError("Author must not be empty.")
        if year < 0:
            raise ValueError("Year must not be negative.")
        if year > MAX_YEAR:
            raise ValueError(f"Year must not exceed {MAX_YEAR}.")
        if STRICT_VALIDATION and title.strip().lower() in self._title_index:
            raise ValueError(f"A book titled '{title.strip()}' already exists.")
        start = time.perf_counter()
        book = Book(title=title.strip(), author=author.strip(), year=year)
        self.books.append(book)
        self._title_index[book.title.lower()] = book
        self._author_index.setdefault(book.author.lower(), []).append(book)
        self.save_books()
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(json.dumps({
            "op": "add_book", "status": "ok",
            "title": book.title,
            "elapsed_ms": round(elapsed_ms, 2),
        }))
        return book

    def list_books(self) -> list[Book]:
        """Return all books in the collection."""
        return self.books

    def find_book_by_title(self, title: str) -> Book | None:
        """Find a book by title. Case-insensitive by default.

        Uses an O(1) dict lookup (case-insensitive mode) instead of
        scanning the full list.
        Set env var BOOK_APP_CASE_SENSITIVE=1 for exact-case matching.
        """
        if CASE_SENSITIVE:
            return next(
                (book for book in self.books if book.title == title),
                None,
            )
        return self._title_index.get(title.lower())

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by title. Returns True if found, False otherwise."""
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            logger.info(json.dumps({
                "op": "mark_as_read", "status": "ok",
                "title": title,
            }))
            return True
        logger.info(json.dumps({
            "op": "mark_as_read", "status": "not_found",
            "title": title,
        }))
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        start = time.perf_counter()
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self._title_index.pop(book.title.lower(), None)
            author_key = book.author.lower()
            if author_key in self._author_index:
                self._author_index[author_key] = [
                    b for b in self._author_index[author_key]
                    if b is not book
                ]
                if not self._author_index[author_key]:
                    del self._author_index[author_key]
            self.save_books()
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info(json.dumps({
                "op": "remove_book", "status": "ok",
                "title": title,
                "elapsed_ms": round(elapsed_ms, 2),
            }))
            return True
        logger.info(json.dumps({
            "op": "remove_book", "status": "not_found",
            "title": title,
        }))
        return False

    def find_by_author(self, author: str) -> list[Book]:
        """Find all books by a given author. O(1) dict lookup."""
        results = self._author_index.get(author.lower(), [])
        logger.info(json.dumps({
            "op": "find_by_author", "status": "ok",
            "author": author,
            "matches": len(results),
        }))
        return results

    def stats(self) -> dict:
        """Return collection health metrics."""
        total = len(self.books)
        read_count = sum(1 for b in self.books if b.read)
        metrics = {
            "total_books": total,
            "read": read_count,
            "unread": total - read_count,
            "unique_authors": len({b.author for b in self.books}),
        }
        logger.info(json.dumps({"op": "stats", **metrics}))
        return metrics
