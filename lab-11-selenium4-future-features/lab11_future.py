import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = Path(__file__).resolve().parent
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler(BASE_DIR / "future_outlook.log", encoding="utf-8"),
                               logging.StreamHandler()])
logger = logging.getLogger(__name__)


def build_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})
    return webdriver.Chrome(options=options)


def relative_locator_demo(driver):
    driver.get("https://the-internet.herokuapp.com/login")
    wait = WebDriverWait(driver, 10)
    username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password = driver.find_element(locate_with(By.TAG_NAME, "input").below(username))
    button = driver.find_element(locate_with(By.TAG_NAME, "button").below(password))
    username.send_keys("demo-user")
    password.send_keys("demo-password")
    logger.info("Relative locators found password=%s button=%s",
                password.get_attribute("id"), button.get_attribute("type"))


def collect_network_responses(driver):
    driver.execute_cdp_cmd("Network.enable", {})
    driver.get("https://httpbin.org/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    responses = []
    for entry in driver.get_log("performance"):
        message = json.loads(entry["message"])["message"]
        if message.get("method") == "Network.responseReceived":
            response = message["params"]["response"]
            responses.append({
                "url": response.get("url"),
                "status": response.get("status"),
                "mime_type": response.get("mimeType")
            })
    output = BASE_DIR / "network_responses.json"
    output.write_text(json.dumps(responses, indent=2), encoding="utf-8")
    logger.info("Captured %d network responses in %s", len(responses), output)


def measure_performance(driver):
    started = time.perf_counter()
    driver.get("https://the-internet.herokuapp.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    elapsed = time.perf_counter() - started
    timing = driver.execute_script("""
        const t = performance.getEntriesByType('navigation')[0];
        return t ? {
            domContentLoaded: t.domContentLoadedEventEnd,
            loadEventEnd: t.loadEventEnd,
            responseEnd: t.responseEnd,
            requestStart: t.requestStart
        } : {};
    """)
    report = {
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "webdriver_navigation_seconds": round(elapsed, 4),
        "navigation_timing_ms": timing
    }
    (BASE_DIR / "performance_metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Performance report: %s", report)


def window_and_screenshot_demo(driver):
    original = driver.current_window_handle
    driver.switch_to.new_window("tab")
    driver.get("https://httpbin.org/user-agent")
    logger.info("User-agent endpoint response: %s", driver.find_element(By.TAG_NAME, "body").text)
    driver.close()
    driver.switch_to.window(original)
    driver.get("https://the-internet.herokuapp.com/")
    driver.save_screenshot(str(BASE_DIR / "homepage.png"))
    header = driver.find_element(By.TAG_NAME, "h1")
    header.screenshot(str(BASE_DIR / "header.png"))


def main():
    driver = build_driver()
    try:
        relative_locator_demo(driver)
        collect_network_responses(driver)
        measure_performance(driver)
        window_and_screenshot_demo(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
