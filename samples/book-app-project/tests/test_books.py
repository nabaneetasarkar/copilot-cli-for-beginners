import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

import books
from books import Book, BookCollection
from utils import format_book_list, get_author_input, get_title_input


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


# --- STRICT_VALIDATION flag tests (Walk Ex 13) ---


def test_strict_validation_off_allows_duplicates(monkeypatch):
    """Flag OFF (default): duplicate titles are allowed."""
    monkeypatch.setattr(books, "STRICT_VALIDATION", False)
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune", "Another Author", 2020)
    assert len(collection.books) == 2


def test_strict_validation_on_rejects_duplicates(monkeypatch):
    """Flag ON: adding a book with an existing title raises ValueError."""
    monkeypatch.setattr(books, "STRICT_VALIDATION", True)
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    with pytest.raises(ValueError, match="already exists"):
        collection.add_book("Dune", "Another Author", 2020)


def test_strict_validation_on_case_insensitive(monkeypatch):
    """Flag ON: duplicate check is case-insensitive."""
    monkeypatch.setattr(books, "STRICT_VALIDATION", True)
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    with pytest.raises(ValueError, match="already exists"):
        collection.add_book("dune", "Another Author", 2020)


def test_save_books_survives_corrupt_load(tmp_path, monkeypatch):
    """Resilience: loading a corrupt file doesn't crash, collection starts empty."""
    corrupt_file = tmp_path / "data.json"
    corrupt_file.write_text("{bad json!!!")
    monkeypatch.setattr(books, "DATA_FILE", str(corrupt_file))
    collection = BookCollection()
    assert collection.books == []
    # Can still add books after corrupt load
    collection.add_book("Recovery Book", "Author", 2024)
    assert len(collection.books) == 1


def test_save_books_atomic_write_on_disk_error(tmp_path, monkeypatch):
    """Failure test: save_books raises OSError after all retries exhausted."""
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))
    monkeypatch.setattr(books, "SAVE_MAX_RETRIES", 2)
    monkeypatch.setattr(books, "SAVE_BACKOFF_BASE", 0)  # no delay in tests
    collection = BookCollection()

    # Simulate disk failure by making mkstemp raise
    import tempfile as _tempfile

    def failing_mkstemp(**kwargs):
        raise OSError("Simulated disk full")

    monkeypatch.setattr(_tempfile, "mkstemp", failing_mkstemp)

    with pytest.raises(OSError, match="after 2 attempts"):
        collection.add_book("Fail Book", "Author", 2024)


def test_save_books_retry_succeeds_after_transient_failure(tmp_path, monkeypatch):
    """Resilience: save_books retries on transient OSError and succeeds."""
    data_file = tmp_path / "data.json"
    data_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))
    monkeypatch.setattr(books, "SAVE_MAX_RETRIES", 3)
    monkeypatch.setattr(books, "SAVE_BACKOFF_BASE", 0)  # no delay in tests
    collection = BookCollection()

    import tempfile as _tempfile

    real_mkstemp = _tempfile.mkstemp
    call_count = {"n": 0}

    def flaky_mkstemp(**kwargs):
        call_count["n"] += 1
        if call_count["n"] <= 1:
            raise OSError("Transient disk error")
        return real_mkstemp(**kwargs)

    monkeypatch.setattr(_tempfile, "mkstemp", flaky_mkstemp)

    # Should succeed on retry despite first failure
    book = collection.add_book("Retry Book", "Author", 2024)
    assert book.title == "Retry Book"
    assert len(collection.books) == 1


# --- format_book_list tests (Walk Ex 3) ---


def test_format_book_list_empty():
    """format_book_list returns 'No books found.' for an empty list."""
    assert format_book_list([]) == "No books found."


def test_format_book_list_with_books():
    """format_book_list formats books with index, title, author, year, status."""
    book_list = [
        Book(title="Dune", author="Frank Herbert", year=1965, read=True),
        Book(title="1984", author="George Orwell", year=1949, read=False),
    ]
    result = format_book_list(book_list)
    assert "1. Dune by Frank Herbert (1965) - Read" in result
    assert "2. 1984 by George Orwell (1949) - Unread" in result


def test_get_title_input_strips_whitespace(monkeypatch):
    """get_title_input strips leading/trailing whitespace from user input."""
    monkeypatch.setattr("builtins.input", lambda _: "  Dune  ")
    assert get_title_input() == "Dune"


def test_get_author_input_strips_whitespace(monkeypatch):
    """get_author_input strips leading/trailing whitespace from user input."""
    monkeypatch.setattr("builtins.input", lambda _: "  Frank Herbert  ")
    assert get_author_input() == "Frank Herbert"


# --- Contract / golden-file tests (Walk Ex 5) ---

GOLDEN_DIR = os.path.join(os.path.dirname(__file__), "golden")


def test_save_produces_golden_json(tmp_path, monkeypatch):
    """Contract: save_books output matches the golden snapshot exactly."""
    data_file = tmp_path / "data.json"
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))

    collection = BookCollection()
    collection.books = [
        Book(title="Dune", author="Frank Herbert", year=1965, read=True),
        Book(title="1984", author="George Orwell", year=1949, read=False),
    ]
    collection.save_books()

    actual = json.loads(data_file.read_text())
    golden_path = os.path.join(GOLDEN_DIR, "books_snapshot.json")
    with open(golden_path) as f:
        expected = json.load(f)

    assert actual == expected, (
        "Saved JSON does not match golden snapshot. "
        "If the change is intentional, update tests/golden/books_snapshot.json"
    )


def test_load_roundtrip_from_golden(tmp_path, monkeypatch):
    """Contract: loading the golden file produces the expected Book objects."""
    import shutil

    golden_path = os.path.join(GOLDEN_DIR, "books_snapshot.json")
    data_file = tmp_path / "data.json"
    shutil.copy(golden_path, data_file)
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))

    collection = BookCollection()
    assert len(collection.books) == 2
    assert collection.books[0].title == "Dune"
    assert collection.books[0].read is True
    assert collection.books[1].title == "1984"
    assert collection.books[1].read is False


def test_golden_schema_keys():
    """Contract: golden file contains exactly the expected keys per book."""
    golden_path = os.path.join(GOLDEN_DIR, "books_snapshot.json")
    with open(golden_path) as f:
        data = json.load(f)

    expected_keys = {"title", "author", "year", "read"}
    for entry in data:
        assert set(entry.keys()) == expected_keys, (
            f"Schema mismatch: expected {expected_keys}, got {set(entry.keys())}"
        )


# --- Contract: stats() API boundary (Run Ex 5) ---


def test_stats_contract_keys():
    """Contract: stats() returns exactly the expected keys."""
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.stats()
    expected_keys = {"total_books", "read", "unread", "unique_authors"}
    assert set(result.keys()) == expected_keys, (
        f"stats() schema mismatch: expected {expected_keys}, got {set(result.keys())}"
    )


def test_stats_contract_types():
    """Contract: stats() values are all integers."""
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("1984", "George Orwell", 1949)
    collection.mark_as_read("Dune")
    result = collection.stats()
    for key, value in result.items():
        assert isinstance(value, int), (
            f"stats()['{key}'] should be int, got {type(value).__name__}"
        )


def test_stats_contract_values():
    """Contract: stats() values are consistent (read + unread == total)."""
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("1984", "George Orwell", 1949)
    collection.mark_as_read("Dune")
    result = collection.stats()
    assert result["total_books"] == result["read"] + result["unread"], (
        "stats() invariant broken: total != read + unread"
    )


# --- Contract: format_book_list display boundary (Run Ex 5) ---


def test_format_book_list_contract_line_pattern():
    """Contract: each book line matches the expected display pattern."""
    import re

    book_list = [
        Book(title="Dune", author="Frank Herbert", year=1965, read=True),
    ]
    result = format_book_list(book_list)
    lines = result.strip().split("\n")
    # First line is header "Your Books:", book lines start at index 1
    book_line = lines[1]
    pattern = r"^\d+\. .+ by .+ \(\d{4}\) - (Read|Unread)$"
    assert re.match(pattern, book_line), (
        f"Display format contract broken. Expected pattern '{pattern}', "
        f"got: '{book_line}'"
    )


# --- Security hardening tests (Run Ex 8) ---


def test_year_upper_bound_rejected():
    """Security: years above MAX_YEAR are rejected."""
    collection = BookCollection()
    with pytest.raises(ValueError, match="must not exceed"):
        collection.add_book("Future Book", "Author", 10000)


def test_year_at_max_accepted():
    """Security: year exactly at MAX_YEAR is accepted."""
    collection = BookCollection()
    book = collection.add_book("Edge Book", "Author", books.MAX_YEAR)
    assert book.year == books.MAX_YEAR


def test_load_rejects_oversized_file(tmp_path, monkeypatch):
    """Security: load_books refuses files exceeding MAX_DATA_FILE_BYTES."""
    big_file = tmp_path / "data.json"
    # Write a valid JSON file larger than the limit
    monkeypatch.setattr(books, "MAX_DATA_FILE_BYTES", 100)
    record = {
        "title": "X" * 200, "author": "A",
        "year": 2000, "read": False,
    }
    big_file.write_text(json.dumps([record]))
    monkeypatch.setattr(books, "DATA_FILE", str(big_file))
    collection = BookCollection()
    assert collection.books == []


def test_load_strips_unknown_keys(tmp_path, monkeypatch):
    """Security: unknown keys in data.json are silently stripped."""
    data_file = tmp_path / "data.json"
    data_file.write_text(json.dumps([
        {"title": "Dune", "author": "Frank Herbert", "year": 1965, "read": False,
         "injected": "malicious", "extra_field": 42}
    ]))
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))
    collection = BookCollection()
    assert len(collection.books) == 1
    assert collection.books[0].title == "Dune"
    assert not hasattr(collection.books[0], "injected")


# --- STRICT_LOAD flag tests (Run Ex 13) ---


def test_strict_load_off_corrupt_recovers(tmp_path, monkeypatch):
    """STRICT_LOAD OFF: corrupt data.json recovers to empty."""
    monkeypatch.setattr(books, "STRICT_LOAD", False)
    data_file = tmp_path / "data.json"
    data_file.write_text("{not valid json")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))
    collection = BookCollection()
    assert collection.books == []


def test_strict_load_on_corrupt_raises(tmp_path, monkeypatch):
    """STRICT_LOAD ON: corrupt data.json raises OSError."""
    monkeypatch.setattr(books, "STRICT_LOAD", True)
    data_file = tmp_path / "data.json"
    data_file.write_text("{not valid json")
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))
    with pytest.raises(OSError, match="corrupted"):
        BookCollection()


def test_strict_load_off_oversized_recovers(tmp_path, monkeypatch):
    """STRICT_LOAD OFF: oversized data.json recovers to empty."""
    monkeypatch.setattr(books, "STRICT_LOAD", False)
    monkeypatch.setattr(books, "MAX_DATA_FILE_BYTES", 50)
    data_file = tmp_path / "data.json"
    record = {
        "title": "X" * 200, "author": "A",
        "year": 2000, "read": False,
    }
    data_file.write_text(json.dumps([record]))
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))
    collection = BookCollection()
    assert collection.books == []


def test_strict_load_on_oversized_raises(tmp_path, monkeypatch):
    """STRICT_LOAD ON: oversized data.json raises OSError."""
    monkeypatch.setattr(books, "STRICT_LOAD", True)
    monkeypatch.setattr(books, "MAX_DATA_FILE_BYTES", 50)
    data_file = tmp_path / "data.json"
    record = {
        "title": "X" * 200, "author": "A",
        "year": 2000, "read": False,
    }
    data_file.write_text(json.dumps([record]))
    monkeypatch.setattr(books, "DATA_FILE", str(data_file))
    with pytest.raises(OSError, match="exceeds"):
        BookCollection()
