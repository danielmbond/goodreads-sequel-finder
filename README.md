# Goodreads Missing Series Finder

A smart automation script that reviews your completed book library history, searches Goodreads to see if authors have published newer sequels or installments in those series, and automatically compiles them into an import-ready tracking list.

## 🚀 How It Works
Since the public Goodreads API is deprecated and automated browser authentications are heavily restricted by security walls, this tool utilizes a safe two-step integration loop:
1. **Reads History Locally**: It parses an offline data export file straight from your account to safely map every completed series book you have ever logged.
2. **Finds Sequels Safely**: It looks up public series indices with structural connection delays to bypass standard network blocks.
3. **Generates Target Import File**: It compiles unread sequel items into a custom CSV configured directly for bulk importing onto your custom online shelf.

## 📋 Features
- **Plug-and-Play Setup**: Self-contained runtime architecture. On execution, it self-diagnoses missing dependencies and attempts to download missing external wrappers automatically.
- **Smart Tracking Matrix**: Maps exactly which entry index you paused at, ignoring older installments while flagging novel entries.
- **Rate Limit Safeguards**: Configured with built-in request spacing and connection pooling to avoid generating aggressive browser connection footprints.

## 🛠️ Step-by-Step Guide

### 1. Create the Target Bookshelf on Goodreads
Goodreads will tag imported books automatically, but if you want your new updates cleanly grouped into an exclusive or specific shelf, it is best to build it first.
1. Log into your account and navigate to **My Books** via the top menu bar.
2. Look at the left sidebar menu under the **Bookshelves** header.
3. Click the **Add Shelf** link at the bottom of your shelf listing.
4. Type exactly `missingseries` into the text prompt box and click **Add**. 

### 2. Download Your Library Data
1. Navigate directly to the [Goodreads Import/Export Dashboard](https://www.goodreads.com/review/import). *(Note: Ensure you are utilizing a desktop browser layout view)*.
2. Hit the **Export Library** option visible in the upper right.
3. Allow up to a minute for creation, select **Download export**, and place the file within your script path directory.
4. Rename this source file exactly to: `goodreads_library_export.csv`

### 3. Run the Script
Execute the program via your operating system terminal:
```bash
python find_series.py
```
The application handles library check routines silently, dynamically reporting identified titles straight to your active console panel. Once complete, it creates an output ledger named `goodreads_missing_series.csv`.

### 4. Update Your Online Book Shelf
1. Revisit the same [Goodreads Import/Export Dashboard](https://www.goodreads.com/review/import).
2. Choose your generated file (`goodreads_missing_series.csv`) and select **Import Books**.
3. All target releases will process in a bulk update batch, instantly loading them straight to your designated `missingseries` shelf online.

## ⚠️ Configuration Alterations
If you want to map targets to a different shelf tag, alter the assignment label directly in the initialization header block of `find_series.py`:
```python
TARGET_SHELF = 'missingseries'  # Swap with any tag name you want
```

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for details.
