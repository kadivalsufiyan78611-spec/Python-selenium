# Lab 4: Introduction to Web Element Identification

## Overview

This lab demonstrates how to identify elements on a web page with Selenium WebDriver using the ID, NAME, and TAG_NAME locator strategies. It also uses JavaScript to highlight elements, saves screenshots, and validates visible heading text.

The target is the public learning site https://the-internet.herokuapp.com/. The site is an external dependency and may change or become unavailable.

## Learning objectives

- Find form fields with `By.ID` and `By.NAME`.
- Find headings and links with `By.TAG_NAME`.
- Use explicit waits for visible or present elements.
- Execute JavaScript to highlight a located element.
- Capture screenshots for visual inspection.
- Validate page text and report a simple pass/fail summary.

## Requirements

- Python 3.10 or newer
- Chrome or Chromium installed
- Internet access
- Selenium 4.x

Selenium Manager, bundled with modern Selenium versions, normally resolves the compatible browser driver automatically.

## Project structure

```text
lab-04-web-element-identification/
├── screenshots/
├── lab4_identification.py
├── requirements.txt
├── README.md
└── DEEP-DIVE.md
```

The `screenshots/` directory is created when the script runs.

## Setup

From this directory, create and activate a virtual environment.

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the lab

```bash
python lab4_identification.py
```

The script opens Chrome, visits the demo login page to demonstrate ID and NAME locators, then visits the home page to demonstrate TAG_NAME. It highlights a sample element during each locator demonstration.

## Expected output and artifacts

The terminal reports located elements, the page heading, the number of links, and a final pass/fail summary. Screenshots are saved under `screenshots/`:

- `id-elements.png`
- `name-elements.png`
- `tag-name-elements.png`

The exact number of links can change when the external website changes. The heading assertion expects the page heading to contain `Welcome to the-internet`.

## Locator strategies

| Strategy | Example | Best use |
|---|---|---|
| ID | `(By.ID, "username")` | A stable, unique element ID |
| NAME | `(By.NAME, "password")` | Form controls with a stable name attribute |
| TAG_NAME | `(By.TAG_NAME, "h1")` | Finding elements by HTML tag; use `find_elements` for collections |

Use the most stable locator available. Tag names are often shared by many elements, so a tag locator may return the first matching element or a collection.

## Troubleshooting

### Chrome or driver fails to start

Confirm Chrome/Chromium is installed and the active Python environment has Selenium installed. Try `python -c "import selenium; print(selenium.__version__)"`. Check network access if Selenium Manager needs to download a driver.

### Element lookup times out

Confirm the target URL loads in a normal browser, inspect the current page HTML, and verify the locator attribute. The script uses explicit waits rather than fixed sleeps.

### Screenshot is missing

Check that the process can write to this directory and inspect the terminal for an exception. Screenshots are stored relative to this script, not the shell's current directory.

### Heading assertion fails

Open the home page and inspect its current heading. The external demo site may have changed its content.

## Cleanup

Remove generated screenshots when you no longer need them:

```bash
rm -f screenshots/*.png
```

Run the command from this lab directory. It only removes generated PNG files inside this lab's screenshots directory.

## Verification checklist

- [ ] Dependencies install in the intended virtual environment.
- [ ] The script starts Chrome and opens the public demo site.
- [ ] ID and NAME locators find the login fields.
- [ ] TAG_NAME locators find the heading and links.
- [ ] Three screenshots are created.
- [ ] The heading assertion and final summary are displayed.

A syntax check does not prove browser automation passed. Only report a live run as successful after running it with a working browser and network access.
