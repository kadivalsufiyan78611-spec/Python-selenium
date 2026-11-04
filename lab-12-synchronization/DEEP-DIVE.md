# Lab 12 — Engineering Deep Dive

## Synchronization model
Browser automation is asynchronous: navigation, JavaScript, network responses, and rendering do not complete at the same instant. A reliable test waits for the state it needs rather than assuming a fixed delay.

## Wait strategies
- No wait: immediate lookup can race the application and fail.
- Implicit wait: affects element location calls, not arbitrary state transitions or visibility of an already-present hidden element.
- Explicit wait: polls a specific expected condition, such as visibility or clickability.
- Fixed sleep: pauses for a predetermined duration regardless of whether the page is ready.

## Isolation
Each comparison uses a new WebDriver instance and page navigation. This avoids implicit-wait configuration from one test affecting another.

## Failure analysis
A timeout can indicate slow network, changed markup, a blocked demo site, or a wrong locator. Inspect the page and browser logs before increasing timeout values blindly.

## Experiments
1. Change the explicit timeout and observe timeout behavior.
2. Replace visibility with presence and compare the result.
3. Record several runs and compare medians.
4. Test a loading spinner with `invisibility_of_element_located`.

## Interview questions
1. Why is an explicit wait more expressive than `time.sleep()`?
2. What does an implicit wait affect?
3. Why should implicit and explicit waits be mixed carefully?
4. How does fresh-driver isolation improve a timing comparison?
