# Lab 7 — Handling Multiple Web Elements in Selenium

## Objective

Use plural element lookup to inspect and interact with groups of elements, toggle checkboxes, extract links, classify URLs, and save structured output.

## Project contents

- lab7_multi_elements.py — main Selenium script.
- requirements.txt — Selenium dependency.
- artifacts/ — generated logs, CSV report, and failure screenshot.

## Prerequisites and setup

Python 3.10+, Chrome or Chromium, and network access to the public demo site.

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r lab-07-multiple-web-elements/requirements.txt
~~~

Windows PowerShell activation: .venv\Scripts\Activate.ps1.

## Run

~~~bash
python lab-07-multiple-web-elements/lab7_multi_elements.py
~~~

Chrome runs headlessly by default. Selenium Manager resolves a compatible driver in supported environments.

## Workflow

1. Locate all checkbox inputs using plural lookup.
2. Record initial states, toggle each checkbox, and verify the state changed.
3. Open the demo homepage and locate all anchors.
4. Extract link text and href attributes.
5. Classify URLs by parsed hostname.
6. Print a summary and save structured records to CSV and logs.

## Outputs

The script creates artifacts/ with a timestamped log, extracted_links.csv, and a timestamped screenshot if the main workflow fails.

The demo homepage can change. Its link count is reported as observed and is not hard-coded.

## Verification checklist

- [ ] Chrome starts and closes.
- [ ] All checkboxes are discovered and each changes state.
- [ ] Homepage anchors are extracted.
- [ ] URLs are classified by hostname.
- [ ] Log and CSV files are created.
- [ ] Failure screenshot is captured when possible.

## Troubleshooting

- Driver startup: verify Chrome is installed and upgrade Selenium.
- No elements: check connectivity, page loading, and selector validity.
- Stale reference: re-query elements after DOM changes; individual stale links are logged and skipped.
- Output cannot be written: ensure the repository directory is writable.

## Cleanup

~~~bash
rm -rf lab-07-multiple-web-elements/artifacts
~~~
