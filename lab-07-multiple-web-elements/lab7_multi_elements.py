import csv
import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / "artifacts"
HOME_URL = "https://the-internet.herokuapp.com/"
CHECKBOX_URL = "https://the-internet.herokuapp.com/checkboxes"


def configure_logging():
    OUTPUT.mkdir(exist_ok=True)
    logger = logging.getLogger("lab7")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    for handler in (
        logging.FileHandler(OUTPUT / f"elements_{datetime.now():%Y%m%d_%H%M%S}.log", encoding="utf-8"),
        logging.StreamHandler(),
    ):
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)


def handle_checkboxes(driver, wait, logger):
    driver.get(CHECKBOX_URL)
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='checkbox']")))
    initial = [element.is_selected() for element in elements]
    print(f"Found {len(elements)} checkboxes")
    for index, (element, old_state) in enumerate(zip(elements, initial), 1):
        element.click()
        new_state = element.is_selected()
        print(f"Checkbox {index}: {old_state} -> {new_state}")
        logger.info("Checkbox %s toggled: %s -> %s", index, old_state, new_state)
        if new_state == old_state:
            raise AssertionError(f"Checkbox {index} did not toggle")
    final = [element.is_selected() for element in elements]
    logger.info("Final checkbox states: %s", final)
    return {"count": len(elements), "initial": initial, "final": final}


def extract_all_links(driver, wait, logger):
    driver.get(HOME_URL)
    elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
    records = []
    for index, element in enumerate(elements, 1):
        try:
            text = element.text.strip() or "[No Text]"
            href = element.get_attribute("href") or ""
            if not href:
                logger.warning("Skipping link %s without href", index)
                continue
            host = (urlparse(href).hostname or "").lower()
            kind = "internal" if host == "the-internet.herokuapp.com" else "external"
            records.append({"index": index, "text": text, "href": href, "type": kind})
        except StaleElementReferenceException:
            logger.warning("Link %s became stale and was skipped", index)
    for record in records:
        print(f"{record['index']}. {record['text']} | {record['href']} | {record['type']}")
    logger.info("Extracted %s links", len(records))
    return records


def analyze_links(records, logger):
    result = {
        "internal": sum(item["type"] == "internal" for item in records),
        "external": sum(item["type"] == "external" for item in records),
        "total": len(records),
    }
    logger.info("Link analysis: %s", result)
    print(f"Internal: {result['internal']} | External: {result['external']} | Total: {result['total']}")
    return result


def save_outputs(records, logger):
    path = OUTPUT / "extracted_links.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["index", "text", "href", "type"])
        writer.writeheader()
        writer.writerows(records)
    for item in records:
        logger.info("Link %s | %s | %s | %s", item["index"], item["text"], item["href"], item["type"])
    logger.info("CSV saved: %s", path)
    return path


def safe_element_interaction(driver, locator_type, locator_value, action="find_single"):
    try:
        if action == "find_multiple":
            return driver.find_elements(locator_type, locator_value)
        if action == "find_single":
            return driver.find_element(locator_type, locator_value)
        raise ValueError("Unsupported action")
    except (WebDriverException, ValueError):
        logging.getLogger("lab7").exception("Element lookup failed")
        return [] if action == "find_multiple" else None


def wait_for_elements(driver, locator_type, locator_value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((locator_type, locator_value)))
    except TimeoutException:
        logging.getLogger("lab7").exception("Timed out waiting for elements")
        return []


def main():
    logger = configure_logging()
    driver = None
    try:
        driver = setup_driver()
        wait = WebDriverWait(driver, 15)
        checkbox_data = handle_checkboxes(driver, wait, logger)
        links = extract_all_links(driver, wait, logger)
        summary = analyze_links(links, logger)
        save_outputs(links, logger)
        print(f"Checkboxes processed: {checkbox_data['count']}")
        print(f"Links extracted: {summary['total']}")
        return 0 if checkbox_data["count"] > 0 and summary["total"] > 0 else 1
    except (WebDriverException, TimeoutException, AssertionError):
        logger.exception("Lab 7 execution failed")
        if driver:
            path = OUTPUT / f"failure_{datetime.now():%Y%m%d_%H%M%S}.png"
            try:
                driver.save_screenshot(str(path))
                logger.info("Failure screenshot saved: %s", path)
            except WebDriverException:
                logger.exception("Screenshot capture failed")
        return 1
    finally:
        if driver:
            driver.quit()
            logger.info("WebDriver closed")


if __name__ == "__main__":
    raise SystemExit(main())
