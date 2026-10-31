# Lab 7 — Deep Dive

## 1. find_element versus find_elements

find_element() returns the first matching element and raises NoSuchElementException when none exists. find_elements() returns a list and gives an empty list when there are no matches. Plural lookup is useful for repeated controls, links, rows, and cards.

## 2. Checkbox state

The script records is_selected() before clicking and verifies that the state changes afterward. Blind toggling is not idempotent; production helpers should set a desired state only when needed.

## 3. Link extraction

Anchor text is read through .text, and the destination through get_attribute("href"). Records are stored as dictionaries. URL classification uses the parsed hostname, avoiding substring-based false positives.

The demo homepage is mutable, so the script reports the observed link count instead of asserting a fixed number.

## 4. CSV and logging

CSV stores portable structured records for spreadsheet or programmatic analysis. Logs capture timestamps, failures, and a detailed extraction trail. Runtime artifacts are kept outside source files.

## 5. Explicit waits and stale references

presence_of_all_elements_located waits until matching elements are present. A DOM update can invalidate an existing WebElement reference. The extraction loop handles stale links individually and continues.

## 6. Failure analysis

| Symptom | Likely cause | Investigation |
|---|---|---|
| Empty checkbox list | Selector mismatch or page not ready | Inspect markup and wait |
| Checkbox unchanged | Overlay, disabled control, or click failure | Check visibility and screenshot |
| Link count differs | Homepage changed | Inspect current CSV |
| Link skipped | Stale DOM reference | Re-query after DOM changes |
| CSV missing | Output directory not writable | Check permissions |
| Driver startup failure | Browser missing or driver resolution blocked | Check Chrome and Selenium Manager |

## 7. Experiments

1. Use an incorrect checkbox selector and observe the timeout.
2. Change the code to set all boxes checked instead of toggling.
3. Filter links by a chosen text phrase.
4. Sort records by URL before writing CSV.
5. Run repeatedly and compare observed link counts.

## 8. Best practices

- Use plural lookup for collections.
- Verify state after interaction.
- Use explicit waits for asynchronous pages.
- Store extracted data in structured records.
- Classify URLs by parsed hostname.
- Handle stale references at a narrow scope.
- Keep runtime artifacts out of source control.

## 9. Interview questions

**What is the difference between find_element and find_elements?**
The first returns one element or raises; the second returns a list that may be empty.

**How do you check a checkbox?**
Use is_selected().

**How do you read a link destination?**
Use get_attribute("href") on its anchor element.

**What causes a stale element reference?**
The stored WebElement no longer represents an element attached to the current DOM.

**Why save records as CSV?**
CSV is portable and can be inspected or processed by other tools.

## Takeaways

Plural element lookup, state verification, structured extraction, and robust logging are foundational for scalable browser automation.
