# goodreads-sequel-finder

Reads a Goodreads library export and finds unread books in series you've already started, using the ISBNdb API. Matches by checking whether the series name appears in the ISBNdb title or `title_long` field — no book number required.

## Files

- `find_series.py` — main script
- `.env` — API key (not committed; copy from `.env.example`)
- `goodreads_library_export.csv` — input; exported from Goodreads (not committed)
- `goodreads_missing_series.csv` — output; import back into Goodreads
- `.series_cache.json` — API response cache (30-day TTL, not committed)

## Setup

Copy `.env.example` to `.env` and add your ISBNdb API key:

```
ISBNDB_API_KEY=your_key_here
```

`requests` and `python-dotenv` are auto-installed on first run.

## Running

```
python find_series.py
```

Expects `goodreads_library_export.csv` in the working directory. Results written to `goodreads_missing_series.csv` tagged with shelf `missingseries` for Goodreads import.

## How it works

1. Parses the CSV for books on the `read` shelf whose titles contain a series tag `(Series Name, #N)`
2. For each unique series, queries ISBNdb (`/books/{series_name}`)
3. Filters results by author last name and series name appearing in the title
4. Any matched title not already in the read list is written to the output CSV
5. Results are cached per series for 30 days to avoid redundant API calls

## Code style

- No comments that describe what the code does — names should do that
- Never use bare `except:` — always `except Exception:` or more specific
- Extract helpers rather than letting functions grow long
- Constants at the top of the file, not inline

## Git

- Remote: `https://github.com/danielmbond/goodreads-sequel-finder`
