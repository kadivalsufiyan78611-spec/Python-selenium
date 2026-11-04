# Lab 14 — Advanced User Interaction Automation

## Goal
Use Selenium ActionChains for hover, drag-and-drop, double-click, and right-click interactions on public demo pages.

## Setup and run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python lab14_user_interactions.py
```

Requires Python 3.10+, Chrome/Chromium, and network access.

## Scenarios
- Hover over a menu item and reveal a submenu.
- Drag an element onto a target and verify the target text changes.
- Double-click and right-click buttons and verify their confirmation messages.

## Outputs
- `user_interactions.log` — timestamped scenario results.
- `interaction_failure.png` — screenshot captured when a WebDriver interaction fails.

## Verification
The script waits for visible menus and confirmation messages instead of assuming that each interaction succeeded. Demo-site markup, overlays, and bot protection can change; investigate a failure rather than treating it as a pass.
