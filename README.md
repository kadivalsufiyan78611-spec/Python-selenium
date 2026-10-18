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

## Setup

Requires Python 3.10+, Chrome or Chromium, and network access.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\\Scripts\\activate`.

Selenium Manager, included with Selenium, manages the compatible browser driver.

## Run

```bash
python lab-01-introduction/lab1_intro_selenium.py
python lab-01-introduction/element_location_demo.py
python lab-01-introduction/assertion_tests.py
python lab-01-introduction/troubleshooting_guide.py
python lab-02-core-interactions/lab2_interactions.py
```

The scripts use public demo pages and are intended for learning. Screenshots are written to the current working directory.
