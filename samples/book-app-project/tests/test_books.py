import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_find_book_by_title_case_insensitive():
    """Deterministic test: find_book_by_title is case-insensitive."""
    collection = BookCollection()
    collection.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
    # Search with different casing — should still find the book
    book = collection.find_book_by_title("the great gatsby")
    assert book is not None
    assert book.title == "The Great Gatsby"
    assert book.author == "F. Scott Fitzgerald"
    assert book.year == 1925
    assert book.read is False


def test_add_book_empty_title_raises():
    """Negative test: adding a book with an empty title raises ValueError."""
    collection = BookCollection()
    with pytest.raises(ValueError, match="Title must not be empty"):
        collection.add_book("", "Some Author", 2024)


def test_add_book_empty_author_raises():
    """Negative test: adding a book with an empty author raises ValueError."""
    collection = BookCollection()
    with pytest.raises(ValueError, match="Author must not be empty"):
        collection.add_book("Some Title", "  ", 2024)


def test_add_book_negative_year_raises():
    """Negative test: adding a book with a negative year raises ValueError."""
    collection = BookCollection()
    with pytest.raises(ValueError, match="Year must not be negative"):
        collection.add_book("Some Title", "Some Author", -1)


def test_find_book_case_insensitive_mode_off(monkeypatch):
    """Toggle OFF (default): find_book_by_title is case-insensitive."""
    monkeypatch.setattr(books, "CASE_SENSITIVE", False)
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    assert collection.find_book_by_title("dune") is not None
    assert collection.find_book_by_title("DUNE") is not None


def test_find_book_case_sensitive_mode_on(monkeypatch):
    """Toggle ON: find_book_by_title requires exact case."""
    monkeypatch.setattr(books, "CASE_SENSITIVE", True)
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    assert collection.find_book_by_title("Dune") is not None
    assert collection.find_book_by_title("dune") is None
    assert collection.find_book_by_title("DUNE") is None
