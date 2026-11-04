# Lab 11 — Engineering Deep Dive

## Relative locators
Selenium 4 relative locators express spatial relationships such as above, below, near, left, and right. They are useful when stable semantic attributes are unavailable, but can become brittle when responsive layouts or page geometry changes. Prefer ID, NAME, or accessible attributes when they are reliable.

## Chrome DevTools Protocol
The script enables the Network domain and reads Chrome performance log entries. It filters for `Network.responseReceived` and stores URL, status, and MIME type. CDP is browser-specific and may evolve; keep it isolated behind a helper and use WebDriver BiDi where a supported cross-browser standard is preferable.

## Performance measurement
Python's `time.perf_counter()` measures elapsed wall-clock time around navigation. The Navigation Timing API exposes browser-side timestamps in milliseconds. These measurements describe a single functional navigation, not throughput, concurrency, or a statistically sound benchmark.

## Window lifecycle
The second tab is opened through Selenium 4's window API, used, closed, and the original handle restored. Always restore a known window handle before continuing.

## Failure analysis
- Relative locator selects an unexpected element: inspect DOM geometry and prefer stable attributes.
- No performance logs: verify Chrome logging capabilities and CDP support.
- Empty network report: confirm the page loaded and that the Network domain was enabled before navigation.
- Screenshot missing: verify write permissions and the current output directory.

## Experiments
1. Repeat navigation several times and report median elapsed time.
2. Filter network events by status code or MIME type.
3. Compare a relative locator with an ID-based locator.
4. Add a resource-timing summary while clearly labeling units.

## Interview questions
1. What problem do relative locators solve?
2. How does CDP differ from WebDriver's standard API?
3. Why use `perf_counter()` for elapsed time?
4. Why is one page-load measurement insufficient for performance conclusions?
