# Lab 3 Deep Dive: Test Architecture and Local CI

## 1. Architecture and rationale

The framework separates responsibilities so tests describe behavior rather than low-level browser mechanics:

- `pages/` owns locators and reusable interactions.
- `tests/` owns scenarios and assertions.
- `conftest.py` manages browser lifecycle and failure artifacts.
- `run_tests.py` standardizes report generation and process exit status.
- `run_ci.sh` performs local preflight checks and delegates to the test runner.

This is a local CI simulation, not a hosted CI workflow or deployment pipeline.

## 2. Page Object Model

`BasePage` centralizes explicit waits and common actions. `LoginPage` owns the URL, locators, and login-specific behavior. If the page's HTML changes, locator updates should normally stay in the page object rather than being duplicated across tests.

Explicit waits synchronize with observable browser state. Fixed sleeps add latency and can still be too short on a slow system.

## 3. Fixture lifecycle and screenshots

The function-scoped driver fixture starts a fresh browser per test to reduce state leakage. Its `finally` block quits the browser even if a test fails. The pytest report hook attempts a screenshot after a failed test call; screenshot errors are recorded without replacing the original test failure.

## 4. Reports and exit codes

Pytest returns a process exit code. The runner preserves that code so a failed suite cannot be reported as successful merely because report generation completed. JUnit XML is machine-readable; HTML is intended for human investigation. Timestamped filenames avoid silently overwriting prior reports.

## 5. CI sequence

1. Confirm the selected Python executable exists.
2. Verify pytest is installed in that environment.
3. Compile project Python files.
4. Run pytest and generate reports.
5. Print report locations and return the test runner's exit status.

Dependencies are installed during explicit setup rather than silently upgraded during each CI run.

## 6. Pre-commit hooks

The installer writes a hook only inside the current repository. It does not stage, commit, push, or alter remote configuration. Hooks can be bypassed with Git's `--no-verify`, so they are a developer convenience, not a security boundary. Hosted CI should independently run tests.

## 7. Failure analysis

| Symptom | Likely cause | Investigation |
|---|---|---|
| `SessionNotCreatedException` | Browser/driver mismatch | Check browser version and Selenium Manager output |
| Missing element or timeout | Locator changed, page not loaded, or network issue | Inspect the DOM and target URL |
| DNS or connection error | Network, proxy, or demo-site outage | Test the URL outside the runner |
| Unknown HTML option | `pytest-html` missing from active environment | Check `python -m pip show pytest-html` |
| Missing screenshot | Browser exited or write failed | Inspect the original traceback and filesystem permissions |
| CI reports success unexpectedly | Exit status not propagated | Compare runner exit status with pytest |

## 8. Safety and reliability

- Use only the documented public demo account for this exercise.
- Never commit personal or production credentials in test data.
- Avoid disabling browser security features; this lab does not need those flags.
- Inspect screenshots and HTML reports before publishing because they can expose page content.
- Treat the public demo site as an external dependency.

## 9. Experiments

1. Change a locator and observe the failure and screenshot behavior.
2. Add a temporary failing assertion in a local working tree, run one test, then revert it.
3. Compare smoke-test output with the full suite.
4. Disconnect network access in a disposable environment and compare a connectivity failure with an assertion failure.
5. Inspect the JUnit XML and HTML report from the same run.

## 10. Best practices

- Keep locators close to the page object they describe.
- Prefer explicit waits tied to meaningful conditions.
- Use isolated browser sessions and always close them.
- Keep test data non-sensitive and externalize it when the suite grows.
- Preserve test exit codes so CI can make reliable decisions.
- Keep generated artifacts out of version control unless there is a specific review need.

## 11. Interview questions

**Why use the Page Object Model?** It separates page-specific locators and actions from test intent, reducing duplication and maintenance cost.

**Why use explicit waits?** They wait for a defined browser condition and are generally more reliable than arbitrary fixed delays.

**Why create JUnit XML?** CI systems can consume it to summarize tests, failures, and errors.

**Why capture screenshots on failure?** They provide visual context for debugging, but do not replace logs or tracebacks.

**What makes a local CI script different from hosted CI?** A local script runs on the developer's machine; hosted CI runs in a configured remote environment and can enforce checks independently.

**Why propagate the test process exit code?** Otherwise automation may report success even when tests fail.

## 12. Takeaways

A useful automation lab is reproducible, isolated, observable, and honest about environmental dependencies. Passing syntax checks proves only that source parses; it does not prove that a browser can reach the demo site or that the live test assertions still match it.
