# goodreads-sequel-finder

Reads a Goodreads library export and finds unread books in series you've already started, using the ISBNdb API.

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

`requests`, `python-dotenv`, and `rapidfuzz` are auto-installed on first run.

## Running

```
python find_series.py
```

Expects `goodreads_library_export.csv` in the working directory. Results written to `goodreads_missing_series.csv` tagged with shelf `missingseries` for Goodreads import.

## How it works

1. Parses the CSV for books on the `read` shelf whose titles contain a series tag `(Series Name, #N)`
2. For each unique series, queries ISBNdb (`/books/{series_name}`) with fallback query variants
3. Filters ISBNdb results by author last name and series name appearing in title or `title_long`
4. Skips compilations: collections, box sets, omnibuses, bundles, numeric ranges (e.g. `1-6`)
5. Checks each remaining title against the full Goodreads library using multi-tier matching (see below)
6. Unmatched titles are written to the output CSV
7. Results are cached per series for 30 days

## Title matching

ISBNdb and Goodreads format titles differently. `_is_already_read` uses three tiers:

1. **Exact** — `b['title'].lower() in read_titles`
2. **Normalized** — both sides run through `_normalize_title`, then exact/prefix/reverse-prefix checked. Normalization strips Goodreads series tags `(Series, #N)` and `(Series #N)`, strips remaining parentheticals (e.g. `(We Are Bob)`), uninverts `"Foo, The"` → `"The Foo"`, removes LitRPG/subtitle noise, strips punctuation, and converts number words to digits
3. **Series-prefix strip** — if ISBNdb stores the title as `[Series] [N]: [BookTitle]` (e.g. `"Zodiac Academy 1: The Awakening"`), strip the series name and leading number then re-run tiers 1–2 on the remainder
4. **Fuzzy fallback** — `rapidfuzz.token_set_ratio` at 85%, guarded so titles with different standalone numbers are never matched (prevents book 1's title from shadowing book 13)

Known limitation: ISBNdb occasionally returns entries like `"The Expanse #1"` with no actual book title — these cannot be matched against Goodreads and must be deleted manually.

## Code style

- No comments that describe what the code does — names should do that
- Never use bare `except:` — always `except Exception:` or more specific
- Extract helpers rather than letting functions grow long
- Constants at the top of the file, not inline

## Git

- Remote: `https://github.com/danielmbond/goodreads-sequel-finder`
