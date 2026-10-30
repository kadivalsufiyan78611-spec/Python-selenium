import logging
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://the-internet.herokuapp.com/"
LOGIN_URL = f"{BASE_URL}login"
USERNAME = "tomsmith"
PASSWORD = "SuperSecretPassword!"
WAIT_SECONDS = 10
OUTPUT_DIR = Path(__file__).resolve().parent / "screenshots"
LOG_FILE = Path(__file__).resolve().parent / "locators.log"

logger = logging.getLogger("lab5")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver

def wait_for_element(driver, locator, clickable=False):
    wait = WebDriverWait(driver, WAIT_SECONDS)
    condition = EC.element_to_be_clickable(locator) if clickable else EC.visibility_of_element_located(locator)
    return wait.until(condition)

def take_screenshot(driver, filename_prefix):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = OUTPUT_DIR / f"{filename_prefix}_{timestamp}.png"
    if not driver.save_screenshot(str(path)):
        raise RuntimeError(f"Screenshot could not be saved: {path}")
    logger.info("Screenshot saved: %s", path)
    return path

def extract_result_message(driver):
    message = WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash"))
    )
    text = message.text.strip()
    logger.info("Page result message: %s", text)
    return text

def locate_login_by_xpath(driver):
    logger.info("Locating login form with XPath")
    username = wait_for_element(driver, (By.XPATH, "//input[@id='username']"))
    password = wait_for_element(driver, (By.XPATH, "//input[@type='password']"))
    button = wait_for_element(driver, (By.XPATH, "//button[@type='submit']"), clickable=True)
    return username, password, button

def locate_login_by_css(driver):
    logger.info("Locating login form with CSS Selector")
    username = wait_for_element(driver, (By.CSS_SELECTOR, "input#username"))
    password = wait_for_element(driver, (By.CSS_SELECTOR, "input[name='password']"))
    button = wait_for_element(driver, (By.CSS_SELECTOR, "button.radius"), clickable=True)
    return username, password, button

def locate_login_by_class_name(driver):
    logger.info("Locating login button with Class Name")
    username = wait_for_element(driver, (By.ID, "username"))
    password = wait_for_element(driver, (By.ID, "password"))
    button = wait_for_element(driver, (By.CLASS_NAME, "radius"), clickable=True)
    return username, password, button

def run_login_scenario(driver, name, locator_function, user, password_value, expected_text):
    logger.info("Starting scenario: %s", name)
    driver.get(LOGIN_URL)
    username, password, button = locator_function(driver)
    username.clear()
    username.send_keys(user)
    password.clear()
    password.send_keys(password_value)
    button.click()
    message = extract_result_message(driver)
    take_screenshot(driver, name.lower().replace(" ", "_"))
    passed = expected_text.casefold() in message.casefold()
    logger.info("%s: %s", "PASS" if passed else "FAIL", name)
    return passed

def test_link_text_locators(driver):
    logger.info("Testing exact and partial link text")
    driver.get(BASE_URL)
    exact_link = wait_for_element(driver, (By.LINK_TEXT, "Form Authentication"), clickable=True)
    partial_link = wait_for_element(driver, (By.PARTIAL_LINK_TEXT, "Form"), clickable=True)
    logger.info("Exact link text: %s", exact_link.text)
    logger.info("Partial link text: %s", partial_link.text)
    exact_link.click()
    wait_for_element(driver, (By.ID, "username"))
    take_screenshot(driver, "link_text_navigation")
    passed = driver.current_url.rstrip("/").endswith("/login")
    logger.info("%s: Link Text navigation", "PASS" if passed else "FAIL")
    return passed

def main():
    logger.info("=== Lab 5: Finding Web Elements by Different Methods ===")
    checks = {}
    driver = None
    try:
        driver = setup_driver()
        logger.info("Headless Chrome started")
        checks["XPath login"] = run_login_scenario(driver, "XPath login", locate_login_by_xpath, USERNAME, PASSWORD, "You logged into a secure area")
        checks["CSS Selector login"] = run_login_scenario(driver, "CSS Selector login", locate_login_by_css, USERNAME, PASSWORD, "You logged into a secure area")
        checks["Class Name login button"] = run_login_scenario(driver, "Class Name login button", locate_login_by_class_name, USERNAME, PASSWORD, "You logged into a secure area")
        checks["Exact and partial Link Text"] = test_link_text_locators(driver)
        driver.get(LOGIN_URL)
        checks["Invalid login error"] = run_login_scenario(driver, "Invalid credentials", locate_login_by_css, "invalid_user", "invalid_password", "Your username is invalid")
    except (TimeoutException, WebDriverException, OSError, RuntimeError) as exc:
        logger.exception("Lab execution failed: %s", exc)
        checks["Unexpected execution error"] = False
    finally:
        if driver is not None:
            driver.quit()
            logger.info("WebDriver closed")
    logger.info("=== Lab 5 Results ===")
    for name, passed in checks.items():
        logger.info("%s - %s", "PASS" if passed else "FAIL", name)
    passed_count = sum(checks.values())
    logger.info("Final result: %s/%s checks passed", passed_count, len(checks))
    return 0 if checks and all(checks.values()) else 1

if __name__ == "__main__":
    raise SystemExit(main())
