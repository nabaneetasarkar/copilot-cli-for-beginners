#!/usr/bin/env python3
"""Local validation script — runs all checks that anyone on the team should run
before pushing.

Usage:
    python validate.py          (from the repo root)
"""

import subprocess
import sys
import os

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK_APP = os.path.join(REPO_ROOT, "samples", "book-app-project")

CHECKS = [
    {
        "name": "pytest — book-app-project",
        "cmd": [sys.executable, "-m", "pytest", "tests/", "-v"],
        "cwd": BOOK_APP,
    },
]


def run_check(check: dict) -> bool:
    print(f"\n{'=' * 60}")
    print(f"  {check['name']}")
    print(f"{'=' * 60}\n")
    result = subprocess.run(check["cmd"], cwd=check["cwd"])
    return result.returncode == 0


def main():
    passed = []
    failed = []

    for check in CHECKS:
        if run_check(check):
            passed.append(check["name"])
        else:
            failed.append(check["name"])

    print(f"\n{'=' * 60}")
    print(f"  RESULTS: {len(passed)} passed, {len(failed)} failed")
    print(f"{'=' * 60}")

    for name in passed:
        print(f"  ✓ {name}")
    for name in failed:
        print(f"  ✗ {name}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
