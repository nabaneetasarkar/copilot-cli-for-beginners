from dataclasses import asdict, dataclass
import json
import logging
import os
import tempfile
import time
from typing import List, Optional

logger = logging.getLogger(__name__)

DATA_FILE = "data.json"
CASE_SENSITIVE = os.environ.get("BOOK_APP_CASE_SENSITIVE", "0") == "1"


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
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        start = time.perf_counter()
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
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
        never leaves a half-written data file.  If the write fails, the
        original file is preserved and an IOError is raised.
        """
        data = json.dumps([asdict(b) for b in self.books], indent=2)
        dir_name = os.path.dirname(os.path.abspath(DATA_FILE))
        try:
            fd, tmp_path = tempfile.mkstemp(
                dir=dir_name, suffix=".tmp", prefix=".books_"
            )
            with os.fdopen(fd, "w") as f:
                f.write(data)
            os.replace(tmp_path, DATA_FILE)
        except OSError as exc:
            # Clean up temp file if it was created
            if "tmp_path" in locals() and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            logger.error(json.dumps({
                "op": "save_books", "status": "error",
                "error": str(exc),
            }))
            raise IOError(f"Failed to save books: {exc}") from exc

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
        start = time.perf_counter()
        book = Book(title=title.strip(), author=author.strip(), year=year)
        self.books.append(book)
        self.save_books()
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(json.dumps({
            "op": "add_book", "status": "ok",
            "title": book.title,
            "elapsed_ms": round(elapsed_ms, 2),
        }))
        return book

    def list_books(self) -> List[Book]:
        """Return all books in the collection."""
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by title. Case-insensitive by default.

        Set env var BOOK_APP_CASE_SENSITIVE=1 for exact-case matching.
        """
        if CASE_SENSITIVE:
            return next(
                (book for book in self.books if book.title == title),
                None,
            )
        return next(
            (book for book in self.books if book.title.lower() == title.lower()),
            None,
        )

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by title. Returns True if found, False otherwise."""
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        start = time.perf_counter()
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
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

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
