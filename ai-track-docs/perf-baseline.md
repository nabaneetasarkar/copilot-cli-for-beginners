# Performance Baseline

## Function Measured

`BookCollection.find_book_by_title` — linear scan over `self.books` with case-insensitive comparison.

## How to Run

```powershell
cd samples/book-app-project
python bench_find.py
```

## Baseline Results (Ex 6)

Machine: Windows, Python 3.14.5
Date: 2026-05-13
Lookups per size: 1,000

| Collection Size | Avg (ns) | Min (ns) | Max (ns) |
|---|---|---|---|
| 10 | 1,578 | 1,100 | 21,600 |
| 100 | 8,128 | 7,400 | 12,700 |
| 500 | 52,302 | 39,300 | 364,500 |

## Variance Notes

- **Min/Avg are stable** across repeated runs (within ~10%)
- **Max spikes** are caused by OS scheduling / GC — expected for nanosecond-scale measurements
- Lookup scales linearly with collection size (~5x from 10→100, ~6x from 100→500), consistent with the O(n) linear scan implementation
- No optimization needed at this scale — sub-millisecond even at 500 books
