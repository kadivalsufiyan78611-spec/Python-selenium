# Lab 13 — Intelligent Synchronization Techniques

## Goal
Build reusable explicit-wait helpers and a bounded retry mechanism, then validate dynamic controls that add/remove elements and enable/disable inputs.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python lab13_intelligent_sync.py
```

Requires Python 3.10+, Chrome/Chromium, and network access.

## Features
- Wait for visibility, clickability, and invisibility.
- Retry transient WebDriver actions with a finite attempt count and delay.
- Verify checkbox removal and restoration.
- Verify that a disabled input becomes enabled, accepts text, and becomes disabled again.

## Outputs
- `intelligent_sync.log` — timestamped steps and retry diagnostics.

## Verification
A successful run should log completion of both dynamic-control scenarios. If the external demo changes, inspect its current DOM and update locators rather than suppressing the failure.
