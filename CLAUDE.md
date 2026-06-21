# goodreads

Script that reads a Goodreads library export and finds unread books in series you've already started, using the Apple iTunes Search API.

## Files

- `find_series.py` — main script
- `goodreads_library_export.csv` — input; exported from Goodreads (not committed)
- `goodreads_missing_series.csv` — output; import back into Goodreads
- `.series_cache.json` — API response cache (30-day TTL, not committed)

## Running

```
python find_series.py
```

`requests` and `python-dotenv` are auto-installed if missing. Copy `.env.example` to `.env` and fill in your ISBNdb API key before running.

## Code style

- No comments that describe what the code does — names should do that
- Never use bare `except:` — always `except Exception:` or more specific
- Extract helpers rather than letting functions grow long
- Constants at the top of the file, not inline

## Git

- Remote: `https://github.com/danielmbond/python.git` (part of the broader `python` repo)
- Force push is fine when local and remote diverge
