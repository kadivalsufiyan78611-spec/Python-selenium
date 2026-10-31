# Lab 6 — Handling Challenges in Web Element Identification

## Objective

Practice browser automation when pages load asynchronously, files must be uploaded, JavaScript interaction is needed, and expected failures must be diagnosed.

## Project contents

- lab6_challenges.py — executable Selenium test suite.
- test_upload.txt — local file-upload fixture.
- requirements.txt — Selenium dependency.
- artifacts/ — generated logs, screenshots, and test report.

## Prerequisites

Python 3.10+, Google Chrome or Chromium, and network access to the public demo site.

## Setup

From the repository root:

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r lab-06-element-identification-challenges/requirements.txt
~~~

Windows PowerShell activation: .venv\Scripts\Activate.ps1.

## Run

~~~bash
python lab-06-element-identification-challenges/lab6_challenges.py
~~~

The browser runs headlessly by default. To watch it, change the WebAutomationChallenges() call to WebAutomationChallenges(headless=False) in main().

## Scenarios

1. Dynamic loading: waits for the loading indicator to disappear and verifies Hello World!.
2. File upload: uploads the fixture using an absolute path and verifies the success heading and filename.
3. JavaScript dropdown: scrolls into view, updates the DOM value, dispatches a change event, and verifies the selection.
4. JavaScript checkbox interaction: inspects rendered dimensions and uses JavaScript click for unchecked visible checkboxes.
5. Error handling: captures an expected missing-element timeout and an attempt to interact with a hidden dynamic element.

## Outputs

The script creates artifacts/ with timestamped logs, diagnostic screenshots, and a test report. Exit code is 0 only when all scenarios pass; otherwise it is 1.

## Verification checklist

- [ ] Dependencies install and Chrome starts.
- [ ] Dynamic content resolves to the expected text.
- [ ] Upload confirms test_upload.txt.
- [ ] Dropdown value is 1.
- [ ] Checkbox interaction completes.
- [ ] Expected failure paths are logged.
- [ ] Report is generated and browser closes.

## Troubleshooting

- Driver startup: verify Chrome is installed and upgrade Selenium; Selenium Manager needs network access where a driver download is required.
- Missing fixture: the script resolves it relative to its own file, not the terminal's working directory.
- Timeout: check connectivity and demo-site markup; increase the wait timeout for slow environments.
- Cannot write output: ensure the lab directory is writable.

## Cleanup

~~~bash
rm -rf lab-06-element-identification-challenges/artifacts
~~~

The tracked upload fixture is intentionally retained.
