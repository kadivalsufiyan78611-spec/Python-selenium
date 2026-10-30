# Lab 5 Deep Dive: Advanced Locator Strategies

## 1. What a locator does

A Selenium locator describes how WebDriver should identify an element in the page DOM. The locator is not the element itself; Selenium evaluates it against the current page when a lookup is performed.

The main lab demonstrates XPath, CSS Selector, Class Name, Link Text, and Partial Link Text. The extended exercise also demonstrates ID, NAME, and TAG_NAME.

## 2. XPath

XPath selects nodes using path expressions and predicates. Examples:

- //input[@id='username']
- //button[@type='submit']
- //form[@id='login']//button[@type='submit']

The first expressions match attributes. The nested expression scopes the button lookup to the form with ID login. Prefer meaningful attributes over positional expressions. Absolute paths and selectors depending on nested layout containers are brittle when page structure changes.

## 3. CSS selectors

CSS selectors provide concise matching by tag, ID, class, and attributes:

- input#username
- input[name='password']
- button.radius
- input[type='text'][name='username']

Standard CSS selectors do not select elements by visible text; use link text or XPath when visible link text is the intended criterion.

## 4. Class Name

The lab finds the submit button using the single class token radius. A class is not necessarily unique. If several elements share it, use a more specific locator. Selenium's Class Name strategy expects one class token; for a combination of classes, use a CSS selector such as button.btn.radius.

## 5. Link Text and Partial Link Text

Link Text matches the complete visible text of an anchor. Partial Link Text matches a substring of visible anchor text. The exercise locates the Form Authentication link from the demo site's home page, clicks it, and verifies navigation to the login page. These strategies can be sensitive to wording and localization changes.

## 6. Synchronization with explicit waits

The scripts use WebDriverWait and expected conditions such as visibility and clickability. A visible element is present and displayed; a clickable element is visible and enabled.

Fixed sleeps pause for a predetermined duration regardless of whether the page is ready. Explicit waits poll for a condition and stop when it becomes true or the timeout expires.

## 7. Logging and diagnostics

The main script logs progress to the terminal and locators.log. The extended script writes to extended_locators.log. Logs record scenario names, result messages, screenshots, and pass/fail status.

Passwords are not written to the logs. This is an important habit even when current values are public demo credentials.

## 8. Login scenarios and result messages

The valid login scenarios use public training credentials and expect a success message. The invalid scenario uses intentionally incorrect values and expects an invalid-username message.

The message extractor waits for the flash message element and returns its visible text. A changed message or site markup can cause a scenario to fail; inspect the current page before modifying an assertion.

## 9. Headless browser execution

Headless Chrome runs without displaying a normal browser window. It is useful for remote machines and automated pipelines. It still requires a working browser binary, compatible driver, and access to the target website.

If a failure is difficult to diagnose, temporarily remove the headless argument and reproduce it in a visible browser session.

## 10. Screenshots

Screenshots are saved to a directory beside the lab scripts. Timestamped names help preserve evidence from multiple scenarios. The extended exercise saves a separate image for its locator checks.

Screenshots are diagnostic artifacts, not proof by themselves that every assertion passed. Review logs and exit status as well.

## 11. Failure analysis

| Symptom | Likely cause | Investigation |
|---|---|---|
| WebDriver startup error | Browser missing, driver resolution failure, or unsupported environment | Verify browser installation, Selenium version, and network access |
| No such element or timeout | Locator no longer matches, page not loaded, or site unavailable | Inspect current DOM and wait condition |
| Link text lookup fails | Visible wording changed or link is absent | Inspect anchor text on the home page |
| Class locator matches wrong control | Class is shared by multiple elements | Add context or use a more specific CSS selector |
| Flash message timeout | Login did not complete or message markup changed | Inspect URL, page content, and browser error output |
| Screenshot not created | Directory permission or browser session problem | Inspect the exception and output directory |

## 12. Experiments

1. Replace an XPath attribute value with a nonexistent value and observe the wait timeout.
2. Use a broad class locator and inspect how many elements share the class.
3. Change exact link text to a partial phrase and compare the two strategies.
4. Run once with headless mode and once with a visible browser.
5. Temporarily change the expected success message and observe the scenario result.
6. Run from a different current working directory and verify that artifacts remain beside the script.

Restore all experimental changes before committing.

## 13. Best practices

- Prefer stable IDs and meaningful attributes where available.
- Use XPath for relationships and DOM expressions that CSS cannot express clearly.
- Keep CSS selectors concise and specific.
- Use Class Name only when the class token identifies the intended element.
- Use link text for navigation when visible wording is stable.
- Use explicit waits for visibility and clickability.
- Never log passwords, tokens, or other secrets.
- Capture screenshots and logs to predictable paths.
- Always close the browser, including when a scenario fails.
- Treat public demo websites as external dependencies that can change.

## 14. Interview questions

**What is the difference between XPath and CSS Selector?** XPath supports path navigation and predicates; CSS selectors match elements by tag, ID, class, and attributes with concise syntax.

**When should Link Text be used?** When locating an anchor by its complete visible text is meaningful and stable.

**What does Partial Link Text do?** It finds an anchor whose visible text contains the supplied phrase.

**Can Class Name accept multiple class names separated by spaces?** No. Use one class token with Class Name, or use a CSS selector for multiple classes.

**Why use explicit waits?** They synchronize the test with a browser condition instead of relying on arbitrary delays.

**What is headless mode?** A browser execution mode without a visible browser window.

**Why capture logs and screenshots?** Logs show execution events and failures; screenshots provide visual context for debugging.

**Does successful Python compilation prove the Selenium test passed?** No. A live browser run is required to verify browser startup, network access, current page structure, and assertions.

## 15. Takeaways

Choosing a locator is a maintainability decision as well as a technical one. Stable attributes, explicit waits, careful logging, meaningful assertions, and predictable diagnostic artifacts make browser automation easier to debug and maintain.
