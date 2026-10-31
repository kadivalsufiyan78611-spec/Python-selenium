# Lab 6 — Deep Dive

## Architecture

WebAutomationChallenges owns the browser, explicit wait, logger, screenshots, scenario methods, and report generation. main() coordinates tests and always closes the browser in finally.

## Explicit waits

The dynamic-loading scenario waits for a clickable Start button, clicks it, waits for the loading indicator to become invisible, then waits for the final heading to become visible. Condition-based waits are more reliable than guessing a fixed sleep duration.

## File upload

Selenium sends a local absolute path to an input type=file element. It does not automate the operating system file-picker dialog. The script validates the fixture before uploading and checks the server confirmation afterward.

## JavaScript executor

The dropdown scenario scrolls the element into view, sets its value, and dispatches a bubbling change event. The checkbox demonstration checks rendered dimensions before using JavaScript click.

JavaScript is a fallback, not the preferred default. Native WebDriver actions preserve normal interactability checks and can expose genuine overlay or timing problems. The demo dropdown is visible; this task demonstrates DOM interaction rather than a hidden dropdown.

## Error handling and reporting

Each scenario records exceptions and captures a screenshot where possible. The report records pass/fail results and a success rate. A non-zero exit status makes the script suitable for a future CI job.

## Failure analysis

| Symptom | Likely cause | Investigation |
|---|---|---|
| Driver startup error | Browser missing or driver resolution blocked | Check Chrome version and Selenium Manager network access |
| Dynamic timeout | Slow network or changed markup | Inspect logs and screenshot |
| Fixture missing | Incomplete checkout or moved file | Confirm fixture beside script |
| Upload verification fails | Remote page or upload changed | Inspect result heading and filename |
| JavaScript selection fails | DOM or event behavior changed | Inspect selected option |
| Screenshot missing | Browser unavailable or output not writable | Check logs and directory permissions |

## Experiments

1. Run with headless=False and observe the browser.
2. Increase the wait timeout.
3. Change the expected dynamic text and confirm assertion failure.
4. Rename the upload fixture and inspect preflight validation.
5. Compare JavaScript dropdown selection with Selenium's native Select class.

## Best practices

- Prefer explicit waits to fixed sleeps.
- Use absolute file paths for uploads.
- Verify outcomes after every important action.
- Use JavaScript only when native WebDriver interaction is insufficient.
- Capture logs and screenshots on failure.
- Close the browser in finally.
- Keep generated artifacts separate from source.

## Interview questions

**Why use explicit waits?** They wait for a condition rather than an arbitrary duration.

**How does Selenium upload a file?** It sends an absolute path to the file input.

**Why dispatch a change event?** It notifies page listeners that a DOM value changed.

**Should JavaScript click be the first choice?** No; native WebDriver interaction is preferred.

**Why use finally for cleanup?** It closes the browser even after an exception.

## Takeaways

Reliable automation combines synchronization, result verification, diagnostics, and predictable resource cleanup.
