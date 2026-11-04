# Lab 13 — Engineering Deep Dive

## Expected conditions
The helpers wrap Selenium's explicit wait mechanism and expose intent in the calling code. Visibility, clickability, and invisibility are different states; choose the one that matches the next action.

## Retry strategy
Retries are bounded and limited to transient WebDriver and timeout exceptions. A retry should not hide deterministic assertion failures, invalid test data, or a broken locator. The delay is short and fixed for this demonstration; production systems may use capped exponential backoff with jitter.

## Dynamic controls
The Remove/Add scenario checks that the checkbox disappears and returns. The Enable/Disable scenario waits for the input's enabled state before typing and verifies the disabled state after the second click.

## Reliability considerations
- Keep retries around idempotent or safely repeatable actions.
- Re-find elements after DOM replacement to avoid stale references.
- Log attempt numbers and the exception class.
- Fail visibly after the retry budget is exhausted.

## Experiments
1. Change retry attempts and delay.
2. Add a stale-element recovery case.
3. Replace fixed retry delay with exponential backoff.
4. Capture screenshots when an expected condition times out.

## Interview questions
1. How do presence, visibility, and clickability differ?
2. When are retries dangerous?
3. Why should assertions generally not be retried?
4. What is a stale element reference?
