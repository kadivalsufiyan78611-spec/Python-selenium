# Lab 5: Finding Web Elements by Different Methods

## Overview

This lab practices locating web elements with XPath, CSS Selector, Class Name, Link Text, and Partial Link Text. It automates a public demo login form, reads success and error messages, runs Chrome in headless mode, captures screenshots, and writes execution logs.

A second script explores ID, NAME, TAG_NAME, nested XPath, and attribute-based CSS selectors.

## Learning objectives

- Use XPath and CSS Selector strategies to locate form controls.
- Locate a button by Class Name.
- Navigate with exact and partial link text.
- Fill forms and click buttons using Selenium.
- Extract visible success and error messages.
- Use explicit waits instead of fixed delays.
- Run Chrome in headless mode.
- Save screenshots and structured log output.

## Prerequisites

- Python 3.10 or newer
- Chrome or Chromium installed
- Internet access to the public demo website
- Basic Python, HTML, and Selenium knowledge

The supplied course describes a preconfigured Al Nafi cloud machine. On another machine, install Python and Chrome/Chromium yourself.

## Project structure

- lab5_locators.py — main locator and login scenarios
- extended_locators_test.py — additional locator checks
- requirements.txt — Python dependency
- README.md — setup and runbook
- DEEP-DIVE.md — concepts and failure analysis
- screenshots/ — generated screenshots
- locators.log and extended_locators.log — generated logs

Logs and screenshots are generated when the scripts run. They are not required in source control.

## Environment setup

Linux/macOS:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

Windows PowerShell:

    py -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

Modern Selenium includes Selenium Manager, which can obtain a compatible browser driver. The lab therefore does not need a separate webdriver-manager dependency.

## Run the main lab

    python lab5_locators.py

The script runs successful login scenarios with XPath, CSS Selector, and Class Name for the submit button. It also checks exact and partial link text navigation and verifies that invalid credentials produce an error message.

The public demo site uses the documented training credentials tomsmith and SuperSecretPassword!. These are public demo credentials, not personal account credentials. Do not replace them with real passwords or commit secrets.

## Run the extended locator exercise

    python extended_locators_test.py

This script checks ID, NAME, TAG_NAME, nested XPath, and an attribute-based CSS selector.

## Outputs

- locators.log: main run's timestamped logs.
- extended_locators.log: extended exercise logs.
- screenshots/: screenshots captured during each scenario.

Inspect output:

    tail -n 30 locators.log
    tail -n 30 extended_locators.log
    ls -lh screenshots/

The exact timestamps and page messages depend on when the scripts run and the external site response.

## Locator reference

| Strategy | Example | Typical use |
|---|---|---|
| XPath | //input[@id='username'] | Attribute, hierarchy, and DOM queries |
| CSS Selector | input[name='password'] | Concise attribute and class matching |
| Class Name | radius | An element with a known single class |
| Link Text | Form Authentication | An anchor with exact visible text |
| Partial Link Text | Form | An anchor whose visible text contains a phrase |
| ID | username | A stable unique identifier |
| NAME | password | Form controls with a stable name |
| TAG_NAME | input | Finding a group of elements by HTML tag |

Class Name accepts one class token, not a compound string such as "btn radius". Use a CSS selector for multiple classes, for example button.btn.radius.

## Verification checklist

- [ ] Dependencies install in the active virtual environment.
- [ ] Chrome starts in headless mode.
- [ ] XPath, CSS, and Class Name scenarios locate the expected login controls.
- [ ] Exact and partial link text locate the navigation link.
- [ ] Valid credentials produce the expected success message.
- [ ] Invalid credentials produce an error message.
- [ ] The extended script finds the expected elements.
- [ ] Log files and screenshots are generated.
- [ ] The scripts exit with a non-zero status when a required check fails.

A source syntax check is not a live browser test. Confirm browser startup, network access, current site markup, and assertions in the target environment before claiming the lab passed end-to-end.

## Troubleshooting

### Chrome or driver startup fails

Check that Chrome/Chromium is installed and that the Python environment has the listed Selenium dependency. Selenium Manager may need network access to resolve a driver. Inspect the exception in the terminal.

### Element lookup times out

The public site may be unavailable, slow, or changed. Open the page manually and inspect the element attributes. Confirm that the locator still matches the current DOM.

### Headless execution behaves differently

Temporarily remove the --headless=new argument to observe the browser. Keep headless mode enabled for the intended automated run.

### Screenshots are missing

The script creates its screenshot directory relative to its own location. Check write permissions and review the log for a screenshot exception.

### Log file is not updated

Confirm the process can write to the lab directory. Close other processes that may be holding the log file open.

## Cleanup

From the lab directory, remove generated artifacts:

    rm -f locators.log extended_locators.log
    rm -f screenshots/*.png

This only removes the generated logs and PNG screenshots in this lab directory.
