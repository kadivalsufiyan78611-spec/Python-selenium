from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT = Path(__file__).resolve().parent
REPORTS_DIR = ROOT / "reports"


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(30)
    try:
        yield browser
    finally:
        browser.quit()


@pytest.fixture(autouse=True)
def ensure_reports_directory():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    browser = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
    if browser is None:
        return
    safe_name = "".join(char if char.isalnum() or char in "-_" else "_" for char in item.name)
    screenshot = REPORTS_DIR / f"screenshot-{safe_name}.png"
    try:
        browser.save_screenshot(str(screenshot))
        report.sections.append(("failure screenshot", str(screenshot)))
    except Exception as exc:
        report.sections.append(("failure screenshot error", str(exc)))
