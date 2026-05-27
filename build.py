#!/usr/bin/env python3
"""
build.py — Subject Notes build script
Reads data/books.yaml and outputs books.json.

Usage:
    python build.py

Requirements:
    pip install pyyaml
"""

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

DATA_FILE = Path(__file__).parent / "data" / "books.yaml"
OUTPUT_FILE = Path(__file__).parent / "books.json"


def main():
    print("Building books.json...")

    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found")
        sys.exit(1)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    books = data.get("books", [])

    # Validate required fields
    errors = []
    valid_books = []
    required = ["id", "title", "authors", "clusters"]

    for book in books:
        missing = [k for k in required if k not in book]
        if missing:
            errors.append(f"{book.get('id', '?')}: missing fields: {missing}")
            continue
        valid_books.append(book)

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
        print()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(valid_books, f, ensure_ascii=False, indent=2)

    print(f"OK: Built {len(valid_books)} books -> books.json")

    if errors:
        print(f"  ({len(errors)} book(s) skipped due to errors)")


if __name__ == "__main__":
    main()
