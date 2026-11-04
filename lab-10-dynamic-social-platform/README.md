# Lab 10 — Dynamic Social Platform Automation

## Goal
Practice dynamic-page navigation, form-field automation, table-row extraction, JavaScript scrolling, logging, and CSV export with Selenium.

## Safety and scope
This lab uses public training/demo pages and synthetic data. The form is populated but not submitted. Table rows are treated as post-like records; row styling only simulates likes/comments/shares. It does **not** log in to a real social network or perform real engagement actions.

## Setup
Python 3.10+, Chrome/Chromium, and network access are required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python lab10_social_media.py
```

On Windows, activate with `.venv\\Scripts\\activate`.

## Outputs
- `output/demo_posts.csv` — captured demo table records.
- `social_media.log` — execution and diagnostic messages.

## Workflow
1. Populate a public practice form using synthetic values without submitting it.
2. Read up to five visible rows from the demo pagination table.
3. Apply a visual browser-only marker to demonstrate interaction targeting.
4. Scroll the page using JavaScript and stop when page height no longer grows.
5. Export the collected records as UTF-8 CSV.

## Verification
Open the CSV and confirm the header and captured rows. Check the log for the number of records collected. Page structure and external demo availability can change; a timeout is a genuine failure, not a successful run.

## Troubleshooting
- **Chrome session fails:** update Chrome and Selenium; check that the browser can start in your environment.
- **Element timeout:** inspect the current demo page and confirm the locator still exists.
- **Empty CSV:** verify that the table has visible rows and that the script has write permission to its folder.
- **Demo site unavailable:** retry later or replace the URL with an approved training page and update the locators.

## Cleanup
Remove the generated `output/` directory and `social_media.log` when no longer needed.
