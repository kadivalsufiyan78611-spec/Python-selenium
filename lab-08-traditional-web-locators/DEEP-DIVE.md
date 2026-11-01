# Lab 8 Deep Dive: Traditional Web Element Locators

## Locator fundamentals
A Selenium locator describes how to find a node in the current DOM. This lab uses XPath, CSS selectors, class name, full link text, and partial link text. Selectors should be understandable, scoped, and stable.

## XPath table extraction
The expression //table[@id='table1']//tr selects descendant rows beneath the table with ID table1. The script inspects each row for th header cells or td data cells and serializes the values separately.

## CLASS_NAME and link text
By.CLASS_NAME accepts one class token, such as button. It is not a general CSS selector; use CSS_SELECTOR for compound classes. LINK_TEXT and PARTIAL_LINK_TEXT target anchor text, not arbitrary buttons. Sample words may not appear on the page, so zero matches are possible.

## CSS versus XPath experiment
Four equivalent queries are measured seven times. Median timings reduce sensitivity to a single noisy sample. Result counts are compared; timing differences are not meaningful if selectors return different counts. Measurements describe one local run, not a universal browser-engine ranking.

## Failure analysis
| Symptom | Likely cause | Response |
|---|---|---|
| No rows | Page changed or table ID differs | Inspect DOM and table ID |
| Stale element | DOM updated after lookup | Query again after update |
| Invalid selector | Malformed CSS/XPath | Validate selector syntax |
| Driver error | Browser/driver mismatch | Update browser and use Selenium Manager |
| No link text match | Phrase absent from anchors | Inspect actual anchor text |

## Experiments
1. Change repetition count and compare medians.
2. Add a selector for a specific table column.
3. Compare an ID selector with equivalent XPath.
4. Change target page and observe link-text availability.

## Best practices
- Prefer stable IDs or concise CSS when they express intent.
- Use XPath for relationships and axes.
- Avoid absolute XPath tied to layout.
- Wait for the relevant page state.
- Compare equivalent result sets before comparing speed.

## Interview questions
**What is XPath?** A language for selecting nodes in XML/HTML structures.

**When is CSS useful?** When a concise selector clearly identifies the target.

**When is XPath useful?** For relationships, axes, and text conditions.

**What does CLASS_NAME accept?** One class token.

**Why compare element counts?** To verify that the compared selectors identify equivalent sets.

**Does one run prove CSS is faster?** No; measurements depend on page, browser, selector, and environment.
