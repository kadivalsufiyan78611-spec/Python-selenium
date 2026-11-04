# Lab 12 — Synchronization in Selenium

## Goal
Compare immediate element lookup, implicit waits, explicit waits, and fixed sleeps against a delayed-loading page.

## Setup and run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python lab12_synchronization.py
```

Requires Python 3.10+, Chrome/Chromium, and network access.

## Test design
Each synchronization strategy gets a fresh browser session and page load so that one method's wait configuration does not leak into another test. The script clicks the Start button, then attempts to read the delayed result.

## Outputs
- `sync_results.json` — one result per strategy with success and elapsed seconds.
- `sync.log` — timestamped execution details.

## Expected interpretation
Immediate lookup may fail because the result is not yet visible. An implicit wait applies to element location and may not wait for an existing but hidden element to become visible. The explicit visibility wait expresses the actual condition. The fixed sleep can pass but always waits the full configured duration.

## Verification
Inspect all four result entries and compare success and elapsed time. Network conditions can change timings; no specific duration is guaranteed.
