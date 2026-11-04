# Lab 11 — Selenium 4 Features and Future Outlook

## Goal
Explore Selenium 4 relative locators, Chrome DevTools Protocol (CDP) performance logs, browser timing APIs, multiple windows, and element screenshots.

## Setup
Python 3.10+, Chrome/Chromium, and network access are required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python lab11_future.py
```

## Demonstrations
- Locate password and submit controls relative to the username field.
- Enable CDP Network events and export response metadata to JSON.
- Measure navigation duration with Python's monotonic performance clock and collect browser Navigation Timing values.
- Open and close a second tab, then capture page and element screenshots.

## Generated artifacts
- `network_responses.json`
- `performance_metrics.json`
- `homepage.png`, `header.png`
- `future_outlook.log`

## Verification and caveats
Check that JSON files parse and contain captured data. Network response counts and timings vary by run and network. CDP commands are Chromium-specific. The browser timing API values are milliseconds; the Python navigation duration is seconds. The script is not a load-testing tool and results should not be compared across unrelated machines as absolute performance scores.
