# Lab 14 — Engineering Deep Dive

## ActionChains
ActionChains builds a sequence of low-level pointer and keyboard actions and sends them to the browser when `perform()` is called. It supports compound gestures such as moving to an element, dragging, double-clicking, and context-clicking.

## Interaction design
The script uses visibility waits before hover and drag operations, then verifies the resulting UI state. This is stronger than merely checking that the WebDriver command returned without throwing an exception.

## Reliability considerations
- Scroll elements into view when necessary.
- Avoid fixed sleeps when a state-based condition is available.
- Re-locate elements after navigation or DOM replacement.
- Capture screenshots on failure to preserve useful evidence.
- Keep browser cleanup in a `finally` block.

## Failure analysis
- Hover submenu missing: menu may be hidden, obstructed, or structurally changed.
- Drag-and-drop not applied: target geometry or HTML5 drag behavior may differ.
- Click message missing: overlay, changed locator, or interaction not delivered.
- Session failure: Chrome/driver mismatch or unsupported runtime environment.

## Experiments
1. Use `move_to_element` plus offset to inspect hover sensitivity.
2. Compare drag-and-drop with click-and-hold/move/release actions.
3. Add keyboard actions such as TAB and ENTER.
4. Run headed mode to observe pointer movement during debugging.

## Interview questions
1. When would you use ActionChains instead of WebElement.click()?
2. How do you verify a drag-and-drop operation?
3. What is the difference between a right-click and a context menu?
4. Why should UI state be asserted after an action?
