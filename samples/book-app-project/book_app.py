import json
import logging
import sys
import time

from books import BookCollection
from utils import format_book_list, get_author_input, get_book_details, get_title_input

logger = logging.getLogger(__name__)

# Global collection instance
collection = BookCollection()


def handle_list():
    start = time.perf_counter()
    books = collection.list_books()
    print(format_book_list(books))
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(json.dumps({
        "op": "cli_list", "status": "ok",
        "count": len(books),
        "elapsed_ms": round(elapsed_ms, 2),
    }))


def handle_add():
    print("\nAdd a New Book\n")

    title, author, year = get_book_details()

    try:
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
        logger.info(json.dumps({
            "op": "cli_add", "status": "ok",
            "title": title,
        }))
    except ValueError as e:
        print(f"\nError: {e}\n")
        logger.warning(json.dumps({
            "op": "cli_add", "status": "validation_error",
            "error": str(e),
        }))


def handle_remove():
    print("\nRemove a Book\n")

    title = get_title_input("Enter the title of the book to remove: ")
    removed = collection.remove_book(title)

    print("\nBook removed if it existed.\n")
    logger.info(json.dumps({
        "op": "cli_remove", "status": "ok" if removed else "not_found",
        "title": title,
    }))


def handle_find():
    print("\nFind Books by Author\n")

    author = get_author_input()
    books = collection.find_by_author(author)

    print(format_book_list(books))
    logger.info(json.dumps({
        "op": "cli_find", "status": "ok",
        "author": author,
        "matches": len(books),
    }))


def show_help():
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    logger.info(json.dumps({
        "op": "cli_dispatch", "command": command,
    }))

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        logger.warning(json.dumps({
            "op": "cli_dispatch", "status": "unknown_command",
            "command": command,
        }))
        show_help()


if __name__ == "__main__":
    main()
