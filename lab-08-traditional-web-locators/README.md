# Lab 8: Traditional Methods for Locating Web Elements

## Objectives
- Extract table rows with XPath and serialize them to JSON.
- Locate elements with CLASS_NAME, LINK_TEXT, and PARTIAL_LINK_TEXT.
- Compare equivalent CSS and XPath queries using repeated timings.
- Generate logs, JSON data, and a Markdown report.

## Requirements
Python 3.10+, Chrome or Chromium, and network access to the demo site.

## Setup
From the repository root:

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r lab-08-traditional-web-locators/requirements.txt

Windows activation: .venv\Scripts\activate. Selenium Manager resolves a compatible driver in supported environments.

## Run

    python lab-08-traditional-web-locators/lab8_traditional_locators.py
    python lab-08-traditional-web-locators/analyze_performance.py
    python lab-08-traditional-web-locators/lab_summary.py

## Outputs
- table_data.json: headers, data rows, source URL, and timestamp.
- performance_comparison.json: selector timings, counts, and count agreement.
- locator_methods.json: observations from CLASS_NAME and LINK_TEXT.
- locator_performance.log: execution log.
- performance_report.md: readable comparison report.

## Implementation
The script waits for table#table1, extracts rows with XPath, separates th and td cells, then measures CSS and XPath selectors seven times. Median timing reduces the influence of a single noisy sample. Element counts are compared before naming a faster selector.

CLASS_NAME accepts one class token, not a compound CSS expression. LINK_TEXT methods search anchor text; the sample words may not exist on the target page, which is a valid zero-match result.

## Interpretation
A single run does not prove that CSS or XPath is universally faster. Browser load, selector complexity, page state, and environment affect results. Prefer the clearest stable locator that identifies the intended element.

## Troubleshooting
- Driver startup: update Chrome/Chromium and rerun with Selenium Manager.
- Timeout: verify access to https://the-internet.herokuapp.com/tables.
- Empty data: inspect the page and confirm table ID table1.
- Missing report: run the main script before analysis.
- Validate JSON with python -m json.tool table_data.json.

## Completion checklist
- [ ] Table extracted to JSON.
- [ ] CLASS_NAME and LINK_TEXT exercised.
- [ ] CSS/XPath timings recorded.
- [ ] Report and summary generated.
