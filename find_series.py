import sys
import subprocess
import csv
import re
import time
import json
import os

for pkg in ('requests', 'python-dotenv'):
    try:
        __import__(pkg.replace('-', '_'))
    except ImportError:
        print(f"Installing {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()

INPUT_FILE = 'goodreads_library_export.csv'
OUTPUT_FILE = 'goodreads_missing_series.csv'
CACHE_FILE = '.series_cache.json'
TARGET_SHELF = 'missingseries'
CACHE_DAYS = 30
DELAY = 1.0
ISBNDB_API_KEY = os.environ['ISBNDB_API_KEY']
ISBNDB_BASE_URL = 'https://api2.isbndb.com'


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_cache(data):
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def _fallback_queries(series_name, author_name):
    clean = re.sub(r'\s+series$', '', series_name, flags=re.IGNORECASE).strip()
    author_last = author_name.split()[-1] if author_name else ""
    return [
        f"{clean} {author_last}",
        author_name,
        re.sub(r'^(the|an|a)\s+', '', clean, flags=re.IGNORECASE).strip(),
    ]


def _search_isbndb(query):
    time.sleep(DELAY)
    resp = requests.get(
        f"{ISBNDB_BASE_URL}/books/{query}",
        headers={'Authorization': ISBNDB_API_KEY},
        timeout=10,
    )
    if resp.status_code != 200:
        return []
    return resp.json().get('books', [])


def _extract_books(books, author_name, series_name):
    found = []
    series_lower = series_name.lower()
    for book in books:
        title = book.get('title', '')
        title_long = book.get('title_long', '') or ''
        authors = book.get('authors', [])
        author_str = ', '.join(authors)

        if author_name and author_name.split()[-1].lower() not in author_str.lower():
            continue

        if series_lower not in title.lower() and series_lower not in title_long.lower():
            continue

        clean_title = re.sub(r'\(.*?\)', '', title).strip()
        if not any(b['title'] == clean_title for b in found):
            found.append({'title': clean_title, 'author': author_str})
    return found


def get_series_from_isbndb(series_name, author_name, cache):
    now = time.time()
    entry = cache.get(series_name, {})
    if (now - entry.get('timestamp', 0)) < CACHE_DAYS * 86400:
        return entry.get('books', [])

    print(f"  -> Searching ISBNdb for: '{series_name}'...")

    try:
        items = _search_isbndb(series_name)

        if not items:
            for term in _fallback_queries(series_name, author_name):
                if not term:
                    continue
                print(f"  -> Retry with query variant: '{term}'...")
                items = _search_isbndb(term)
                if items:
                    break

        books = _extract_books(items, author_name, series_name)
        cache[series_name] = {'timestamp': now, 'books': books}
        save_cache(cache)
        return books

    except Exception as e:
        print(f"  -> Error: {e}")
        return []


def read_library(path):
    read_series = {}
    read_titles = set()
    with open(path, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            title = row.get('Title', '')
            author = row.get('Author', '')
            read_titles.add(title.lower())

            if row.get('Exclusive Shelf') != 'read':
                continue

            match = re.search(r'\(([^)]+),\s*#([\d.]+)\)', title)
            if match:
                s_name = match.group(1).strip()
                if s_name not in read_series:
                    read_series[s_name] = {'author': author}

    return read_series, read_titles


def write_output(path, books):
    unique = list({b['title']: b for b in books}.values())
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Author', 'Bookshelves'])
        for b in unique:
            writer.writerow([b['title'], b['author'], TARGET_SHELF])
    return len(unique)


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        sys.exit(1)

    print(f"Reading {INPUT_FILE}...")
    read_series, read_titles = read_library(INPUT_FILE)

    cache = load_cache()
    missing = []

    print(f"Scanning {len(read_series)} series...")
    for i, (s_name, data) in enumerate(read_series.items(), 1):
        print(f"[{i}/{len(read_series)}] Checking: {s_name}")
        books = get_series_from_isbndb(s_name, data['author'], cache)
        for b in books:
            if b['title'].lower() not in read_titles:
                print(f"  -> FOUND: {b['title']}")
                missing.append(b)

    if missing:
        count = write_output(OUTPUT_FILE, missing)
        print(f"\nDone! Saved {count} books to {OUTPUT_FILE}")
    else:
        print("\nAll caught up!")


if __name__ == "__main__":
    main()
