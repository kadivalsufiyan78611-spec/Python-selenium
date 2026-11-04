# Python Selenium Labs

Hands-on browser automation examples using Python and Selenium WebDriver.

## Labs

### Lab 1 — Introduction to Python Selenium
- `lab-01-introduction/lab1_intro_selenium.py`: open a website, inspect page elements, and save a screenshot.
- `lab-01-introduction/element_location_demo.py`: locate elements using IDs, CSS selectors, XPath, and link text.
- `lab-01-introduction/assertion_tests.py`: verify page title and visible page content.
- `lab-01-introduction/troubleshooting_guide.py`: demonstrate safer element lookup and common Selenium errors.

### Lab 2 — WebDriver and Core Interactions
- `lab-02-core-interactions/lab2_interactions.py`: automate a demo login, dropdowns, checkboxes, JavaScript alerts, dynamic content, and screenshots.

### Lab 3 — Case Study and Local CI
- [Lab 3 README](lab-03-case-study-local-ci/README.md): setup, commands, scenarios, reporting, troubleshooting, and cleanup.
- [Lab 3 Deep Dive](lab-03-case-study-local-ci/DEEP-DIVE.md): architecture, failure analysis, experiments, best practices, and interview questions.

### Lab 4 — Web Element Identification
- [Lab 4 README](lab-04-web-element-identification/README.md)
- [Lab 4 Deep Dive](lab-04-web-element-identification/DEEP-DIVE.md)

### Lab 5 — Advanced Locator Strategies
- [Lab 5 README](lab-05-advanced-locators/README.md)
- [Lab 5 Deep Dive](lab-05-advanced-locators/DEEP-DIVE.md)

### Lab 6 — Handling Element Identification Challenges
- [Lab 6 README](lab-06-element-identification-challenges/README.md)
- [Lab 6 Deep Dive](lab-06-element-identification-challenges/DEEP-DIVE.md)

### Lab 7 — Handling Multiple Web Elements
- [Lab 7 README](lab-07-multiple-web-elements/README.md)
- [Lab 7 Deep Dive](lab-07-multiple-web-elements/DEEP-DIVE.md)

### Lab 8 — Traditional Methods for Locating Web Elements
- [Lab 8 README](lab-08-traditional-web-locators/README.md)
- [Lab 8 Deep Dive](lab-08-traditional-web-locators/DEEP-DIVE.md)

### Lab 9 — AI-Powered Element Locators
- [Lab 9 README](lab-09-ai-powered-element-locators/README.md)
- [Lab 9 Deep Dive](lab-09-ai-powered-element-locators/DEEP-DIVE.md)

### Lab 10 — Dynamic Social Platform Automation
- [Lab 10 README](lab-10-dynamic-social-platform/README.md)
- [Lab 10 Deep Dive](lab-10-dynamic-social-platform/DEEP-DIVE.md)
- Main script: `lab-10-dynamic-social-platform/lab10_social_media.py`

### Lab 11 — Selenium 4 Features and Future Outlook
- [Lab 11 README](lab-11-selenium4-future-features/README.md)
- [Lab 11 Deep Dive](lab-11-selenium4-future-features/DEEP-DIVE.md)
- Main script: `lab-11-selenium4-future-features/lab11_future.py`

### Lab 12 — Synchronization in Selenium
- [Lab 12 README](lab-12-synchronization/README.md)
- [Lab 12 Deep Dive](lab-12-synchronization/DEEP-DIVE.md)
- Main script: `lab-12-synchronization/lab12_synchronization.py`

### Lab 13 — Intelligent Synchronization Techniques
- [Lab 13 README](lab-13-intelligent-synchronization/README.md)
- [Lab 13 Deep Dive](lab-13-intelligent-synchronization/DEEP-DIVE.md)
- Main script: `lab-13-intelligent-synchronization/lab13_intelligent_sync.py`

### Lab 14 — Advanced User Interaction Automation
- [Lab 14 README](lab-14-advanced-user-interactions/README.md)
- [Lab 14 Deep Dive](lab-14-advanced-user-interactions/DEEP-DIVE.md)
- Main script: `lab-14-advanced-user-interactions/lab14_user_interactions.py`

## Environment

Requires Python 3.10+, Chrome or Chromium, and network access. Each lab has its own requirements file so dependencies remain isolated.

Example setup:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r lab-12-synchronization/requirements.txt
python lab-12-synchronization/lab12_synchronization.py
```

On Windows, activate with `.venv\\Scripts\\activate`.

Selenium Manager (included with Selenium 4) manages a compatible browser driver in typical environments. Some restricted cloud environments may require a separately installed ChromeDriver.

## Verification policy

Scripts are structured for reproducible learning, but external demo websites, browser versions, and network conditions can change. A GitHub push does not mean the browser scenarios were executed successfully. Run each script in a configured environment and inspect its logs and generated artifacts.
