import logging
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).resolve().parent
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler(BASE_DIR / "sync.log", encoding="utf-8"),
                               logging.StreamHandler()])
logger = logging.getLogger(__name__)
URL = "https://the-internet.herokuapp.com/dynamic_loading/2"


def build_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def reset_page(driver):
    driver.get(URL)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button")))


def run_case(label, action):
    driver = build_driver()
    try:
        reset_page(driver)
        start = time.perf_counter()
        driver.find_element(By.CSS_SELECTOR, "#start button").click()
        try:
            result = action(driver)
            elapsed = time.perf_counter() - start
            logger.info("%s: success=%s elapsed=%.3fs result=%r", label, bool(result), elapsed, result)
            return {"method": label, "success": bool(result), "seconds": round(elapsed, 3)}
        except (NoSuchElementException, TimeoutException) as exc:
            elapsed = time.perf_counter() - start
            logger.info("%s: expected timing failure after %.3fs: %s", label, elapsed, exc.__class__.__name__)
            return {"method": label, "success": False, "seconds": round(elapsed, 3)}
    finally:
        driver.quit()


def without_wait(driver):
    return driver.find_element(By.CSS_SELECTOR, "#finish h4").text


def with_implicit_wait(driver):
    driver.implicitly_wait(8)
    return driver.find_element(By.CSS_SELECTOR, "#finish h4").text


def with_explicit_wait(driver):
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4"))
    )
    return element.text


def with_fixed_sleep(driver):
    time.sleep(6)
    return driver.find_element(By.CSS_SELECTOR, "#finish h4").text


def main():
    cases = [
        ("no_wait", without_wait),
        ("implicit_wait", with_implicit_wait),
        ("explicit_wait", with_explicit_wait),
        ("fixed_sleep", with_fixed_sleep)
    ]
    results = [run_case(name, action) for name, action in cases]
    logger.info("Summary: %s", results)
    (BASE_DIR / "sync_results.json").write_text(
        __import__("json").dumps(results, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
