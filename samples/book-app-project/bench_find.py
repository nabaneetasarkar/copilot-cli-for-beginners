"""Micro-benchmark for BookCollection.find_book_by_title.

Run from the book-app-project directory:
    python bench_find.py

Measures average lookup time across varying collection sizes.
Does NOT modify any production code — read-only benchmark.
"""

import os
import tempfile
import time

# Patch DATA_FILE before importing BookCollection
import books

_bench_dir = tempfile.mkdtemp()
_bench_file = os.path.join(_bench_dir, "data.json")
with open(_bench_file, "w") as _f:
    _f.write("[]")
books.DATA_FILE = _bench_file

from books import BookCollection


def run_benchmark(num_books: int, num_lookups: int = 1000) -> dict:
    """Benchmark find_book_by_title with a collection of num_books."""
    collection = BookCollection()

    # Populate collection directly (skip save_books for speed)
    for i in range(num_books):
        collection.books.append(
            books.Book(title=f"Book {i}", author=f"Author {i}", year=2000 + (i % 26))
        )

    target_title = f"Book {num_books - 1}"  # worst case: last book

    # Warm up
    collection.find_book_by_title(target_title)

    # Measure
    times = []
    for _ in range(num_lookups):
        start = time.perf_counter_ns()
        collection.find_book_by_title(target_title)
        elapsed = time.perf_counter_ns() - start
        times.append(elapsed)

    avg_ns = sum(times) / len(times)
    min_ns = min(times)
    max_ns = max(times)

    return {
        "collection_size": num_books,
        "lookups": num_lookups,
        "avg_ns": round(avg_ns),
        "min_ns": min_ns,
        "max_ns": max_ns,
    }


if __name__ == "__main__":
    sizes = [10, 100, 500, 1000]
    print("find_book_by_title benchmark")
    print(f"{'Size':>6}  {'Avg (ns)':>10}  {'Min (ns)':>10}  {'Max (ns)':>10}")
    print("-" * 44)

    for size in sizes:
        result = run_benchmark(size)
        print(
            f"{result['collection_size']:>6}  "
            f"{result['avg_ns']:>10,}  "
            f"{result['min_ns']:>10,}  "
            f"{result['max_ns']:>10,}"
        )

    # Clean up temp directory
    import shutil
    shutil.rmtree(_bench_dir, ignore_errors=True)
