# Lab 10 — Engineering Deep Dive

## Design
The script separates browser setup, form interaction, record collection, visual simulation, scrolling, and export. This makes each responsibility independently inspectable and easier to troubleshoot.

## Locator and synchronization choices
The form uses NAME locators because the practice form exposes stable field names. A WebDriverWait checks visibility before typing. The table is located by ID and its rows by CSS selector. The script captures only the first five visible rows to keep the exercise deterministic.

## Dynamic content and scrolling
JavaScript reads `document.body.scrollHeight` and scrolls to the bottom. The loop compares the new height with the previous height and exits when no growth is observed. A fixed pause is used only to allow the demo page to react; production workflows should wait for a specific loading indicator or newly rendered element.

## Data handling
CSV output uses an explicit field order, UTF-8 encoding, and `newline=""` to avoid extra blank lines on Windows. Timestamps are recorded in UTC so records from different environments can be compared.

## Important distinction
A row highlight is not a real like, comment, or share. The exercise demonstrates element targeting and JavaScript execution without sending actions to an account or affecting third-party users.

## Failure analysis
- Timeout: page structure changed, network delay, or selector mismatch.
- No rows: pagination table did not load or returned an empty dataset.
- CSV write error: output directory permissions or file lock.
- Browser startup error: Chrome/driver compatibility or missing system dependencies.

## Experiments
1. Change the record limit and compare output size.
2. Add a wait for a known table row instead of relying on a fixed delay.
3. Add a deduplication key before appending records.
4. Compare JavaScript scrolling with scrolling a specific container element.

## Interview questions
1. Why should explicit waits be preferred over long fixed sleeps?
2. What is the difference between DOM presence and visibility?
3. Why is CSV written with `newline=""`?
4. Why should automation against social platforms avoid unauthorized engagement?
