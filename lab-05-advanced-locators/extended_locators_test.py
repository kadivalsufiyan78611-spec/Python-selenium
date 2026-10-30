import logging
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOGIN_URL = "https://the-internet.herokuapp.com/login"
OUTPUT_DIR = Path(__file__).resolve().parent / "screenshots"
LOG_FILE = Path(__file__).resolve().parent / "extended_locators.log"
WAIT_SECONDS = 10

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8", mode="w"), logging.StreamHandler()])
logger = logging.getLogger("extended_lab5")

def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver

def main():
    driver = None
    checks = {}
    try:
        driver = create_driver()
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, WAIT_SECONDS)
        checks["ID locator"] = wait.until(EC.visibility_of_element_located((By.ID, "username"))) is not None
        logger.info("Username located by ID")
        checks["NAME locator"] = wait.until(EC.visibility_of_element_located((By.NAME, "password"))) is not None
        logger.info("Password located by NAME")
        inputs = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
        checks["TAG_NAME locator"] = len(inputs) >= 2
        logger.info("Found %s input elements by TAG_NAME", len(inputs))
        checks["Nested XPath"] = driver.find_element(By.XPATH, "//form[@id='login']//button[@type='submit']").is_displayed()
        logger.info("Submit button located by nested XPath")
        checks["Attribute CSS selector"] = driver.find_element(By.CSS_SELECTOR, "input[type='text'][name='username']").is_displayed()
        logger.info("Username located by attribute CSS selector")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        screenshot = OUTPUT_DIR / "extended_locator_checks.png"
        driver.save_screenshot(str(screenshot))
        logger.info("Screenshot saved: %s", screenshot)
    except (TimeoutException, WebDriverException, OSError) as exc:
        logger.exception("Extended locator test failed: %s", exc)
        checks["Unexpected execution error"] = False
    finally:
        if driver is not None:
            driver.quit()
    for name, passed in checks.items():
        logger.info("%s - %s", "PASS" if passed else "FAIL", name)
    passed_count = sum(checks.values())
    logger.info("Extended result: %s/%s checks passed", passed_count, len(checks))
    return 0 if checks and all(checks.values()) else 1

if __name__ == "__main__":
    raise SystemExit(main())
