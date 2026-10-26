# Lab 3: Case Study and Local Continuous Integration

## Overview

Build a maintainable Selenium test suite for the public demo login page at `https://the-internet.herokuapp.com/login`. The lab uses pytest fixtures, the Page Object Model, explicit waits, failure screenshots, JUnit XML and HTML reports, and a local CI runner. An optional Git pre-commit hook is included.

The target is a third-party demo site. Tests need network access and may fail if the site is unavailable or changes. Do not use personal or production credentials.

## Learning objectives

- Organize browser automation with the Page Object Model.
- Use explicit waits instead of fixed sleeps.
- Cover successful, invalid, and empty login attempts.
- Capture screenshots on test failures and generate reports.
- Run syntax checks and tests with reliable exit-code propagation.
- Install and verify an optional local pre-commit hook.

## Prerequisites

- Python 3.10 or newer
- Git and a POSIX-compatible shell for shell scripts
- Chrome or Chromium
- Internet access for Selenium Manager and the public demo site

Selenium Manager resolves a compatible browser driver on first run. Offline environments may require a manually configured driver.

## Project structure

```text
lab-03-case-study-local-ci/
├── pages/
│   ├── __init__.py
│   └── login_page.py
├── tests/
│   └── test_login.py
├── scripts/
│   ├── install_pre_commit_hook.sh
│   ├── notify_results.sh
│   └── view_results.sh
├── reports/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── run_ci.sh
├── run_tests.py
└── test_data.json
```

## Setup and run

Run these commands from this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -v
python -m pytest -m smoke -v
python -m pytest -m regression -v
python run_tests.py
./run_ci.sh
```

On Windows, activate the environment with `.venv\\Scripts\\activate`; the shell scripts and optional hook target Linux/macOS or a compatible shell.

`run_tests.py` creates timestamped JUnit XML and HTML reports under `reports/`. `run_ci.sh` checks Python syntax, runs the test runner, and returns a non-zero status when a check fails. Syntax validation alone does not prove browser tests pass.

## Test coverage

| Scenario | Expected behavior |
|---|---|
| Valid username and password | Secure area appears and logout link is visible |
| Invalid username and password | Error indicates invalid username |
| Empty username and password | Login is rejected with an error |
| Invalid username with valid password | Login is rejected |
| Valid username with invalid password | Error indicates invalid password |

Assertions reflect the demo site's expected behavior and may need updates if that site changes.

## Failure screenshots and reports

- A screenshot is attempted for failed test calls and saved under `reports/`.
- JUnit XML is machine-readable; HTML is useful for manual investigation.
- Screenshots and HTML reports can contain page data. Review artifacts before sharing them.

## Optional pre-commit hook

```bash
./scripts/install_pre_commit_hook.sh
```

The hook runs `run_ci.sh` before a commit. It may slow commits because browser tests run locally. Remove it with `rm .git/hooks/pre-commit` if no longer wanted. Hooks are local and are not automatically installed for other contributors.

## Troubleshooting

### Chrome or driver cannot start
Confirm Chrome/Chromium is installed, then run `python -c "from selenium import webdriver; d=webdriver.Chrome(); d.quit()"` to isolate driver setup. Check network access if Selenium Manager needs to download a driver.

### Tests time out or cannot reach the demo site
Open the target URL in a browser and check DNS, proxy, and firewall access. A site outage is not proof that the test logic is broken.

### HTML report option is unknown
Run `python -m pip show pytest-html` in the active environment and reinstall dependencies with `python -m pip install -r requirements.txt`.

### No screenshot appears
Screenshot capture is best-effort. A crashed or terminated browser may prevent capture; inspect the original test traceback first.

## Cleanup

```bash
rm -f reports/junit-*.xml reports/report-*.html reports/screenshot-*.png reports/ci-results.txt
```

This removes only generated artifacts in this lab's `reports/` directory.

## Verification checklist

- [ ] Dependencies are installed in the intended virtual environment.
- [ ] `python -m compileall -q pages tests conftest.py run_tests.py` succeeds.
- [ ] `python -m pytest -m smoke -v` completes against the demo site.
- [ ] `python run_tests.py` creates JUnit and HTML reports.
- [ ] A temporary failing test demonstrates screenshot capture; revert the experiment afterward.
- [ ] `./run_ci.sh` returns the same pass/fail status as the test runner.
- [ ] The optional hook is installed only if desired.

Do not claim browser tests passed unless they were actually run with a working browser and network access.
