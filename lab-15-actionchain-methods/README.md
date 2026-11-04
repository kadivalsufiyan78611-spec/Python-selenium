# Lab 15 — Key Methods in ActionChains

## Goal
Practice Selenium ActionChains for keyboard input, drag gestures, modifier-key selection, hover, context-click, and double-click.

## Setup
Requires Python 3.10+, Chrome or Chromium, and network access.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run
```bash
python lab15_actionchains.py
python extended_actionchain_tests.py
python generate_report.py
```

## Scenarios
- Send keyboard keys to a key-press demo page.
- Drag an element using click-and-hold, move, and release.
- Use CTRL-click to select multiple items in a local HTML fixture.
- Exercise keyboard shortcuts, hover, context-click, and double-click.
- Generate a text report from execution logs.

## Outputs
`actionchain_methods.log`, `extended_actionchain.log`, `multiple_selection.html`, `keyboard_test.html`, and `actionchain_lab_report.txt`.

## Verification
The local multi-selection scenario asserts four selected items. The double-click scenario waits for a confirmation message. External demo websites can change; investigate failures rather than assuming a pass.

## Troubleshooting
Check Chrome availability, locator accuracy, overlays, scrolling, and explicit waits. Always call `.perform()` to execute an ActionChains sequence and pair modifier `key_down()` with `key_up()`. Clipboard behavior depends on browser and operating-system permissions; this lab does not claim that a clipboard paste succeeded.
