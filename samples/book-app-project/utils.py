import json
import logging

logger = logging.getLogger(__name__)


def print_menu():
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    return input("Choose an option (1-5): ").strip()


def get_book_details():
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        logger.warning(json.dumps({
            "op": "get_book_details", "status": "invalid_year",
            "raw_input": year_input,
        }))
        year = 0

    logger.info(json.dumps({
        "op": "get_book_details", "status": "ok",
        "title": title, "author": author, "year": year,
    }))
    return title, author, year


def get_title_input(prompt: str = "Enter the title of the book: ") -> str:
    """Prompt for and return a stripped book title."""
    return input(prompt).strip()


def get_author_input(prompt: str = "Author name: ") -> str:
    """Prompt for and return a stripped author name."""
    return input(prompt).strip()


def format_book_list(books) -> str:
    """Format a list of Book objects into a human-readable string.

    Returns the formatted string (does not print).
    """
    if not books:
        return "No books found."

    lines = ["\nYour Books:"]
    for index, book in enumerate(books, start=1):
        status = "Read" if book.read else "Unread"
        lines.append(
            f"{index}. {book.title} by {book.author} ({book.year}) - {status}"
        )
    return "\n".join(lines)


def print_books(books):
    """Print formatted book list. Delegates to format_book_list."""
    print(format_book_list(books))
