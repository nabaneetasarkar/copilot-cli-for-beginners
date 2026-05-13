import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


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
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

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
        book = Book(title=title.strip(), author=author.strip(), year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books in the collection."""
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by title (case-insensitive). Returns None if not found."""
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
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
