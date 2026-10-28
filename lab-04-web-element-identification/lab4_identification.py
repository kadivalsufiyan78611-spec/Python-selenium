from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://the-internet.herokuapp.com/"
LOGIN_URL = f"{BASE_URL}login"
OUTPUT_DIR = Path(__file__).resolve().parent / "screenshots"
WAIT_SECONDS = 10


def setup_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(0)
    return driver


def highlight_element(driver, element, label):
    driver.execute_script(
        """
        arguments[0].style.border = '3px solid red';
        arguments[0].style.backgroundColor = 'yellow';
        arguments[0].style.boxShadow = '0 0 10px red';
        """,
        element,
    )
    print(f"Highlighted: {label}")


def save_screenshot(driver, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT_DIR / filename
    if not driver.save_screenshot(str(destination)):
        raise RuntimeError(f"Could not save screenshot: {destination}")
    print(f"Screenshot saved: {destination}")


def locate_by_id(driver):
    print("\n=== LOCATOR: ID ===")
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, WAIT_SECONDS)
    username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
    password = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    print(f"Username tag: {username.tag_name}")
    print(f"Username placeholder: {username.get_attribute('placeholder')}")
    print(f"Password input type: {password.get_attribute('type')}")
    highlight_element(driver, username, "username input")
    save_screenshot(driver, "id-elements.png")
    return username, password


def locate_by_name(driver):
    print("\n=== LOCATOR: NAME ===")
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, WAIT_SECONDS)
    username = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    password = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    print(f"Username ID: {username.get_attribute('id')}")
    print(f"Password ID: {password.get_attribute('id')}")
    highlight_element(driver, password, "password input")
    save_screenshot(driver, "name-elements.png")
    return username, password


def locate_by_tag_name(driver):
    print("\n=== LOCATOR: TAG NAME ===")
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, WAIT_SECONDS)
    heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
    links = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
    print(f"Main heading: {heading.text.strip()!r}")
    print(f"Links found: {len(links)}")
    visible_links = [link.text.strip() for link in links if link.text.strip()]
    for index, link_text in enumerate(visible_links[:5], start=1):
        print(f"{index}. {link_text}")
    highlight_element(driver, heading, "main heading")
    save_screenshot(driver, "tag-name-elements.png")
    return heading, links


def validate_text(element, expected_text, description):
    actual_text = element.text.strip()
    passed = expected_text.casefold() in actual_text.casefold()
    status = "PASSED" if passed else "FAILED"
    print(f"{status}: {description}; expected {expected_text!r}, got {actual_text!r}")
    return passed


def run_lab(driver):
    results = {}
    try:
        username, password = locate_by_id(driver)
        results["ID locator finds both login fields"] = bool(username and password)
    except (NoSuchElementException, TimeoutException, WebDriverException) as exc:
        print(f"ID locator check failed: {exc}")
        results["ID locator finds both login fields"] = False

    try:
        username, password = locate_by_name(driver)
        results["NAME locator finds both login fields"] = bool(username and password)
    except (NoSuchElementException, TimeoutException, WebDriverException) as exc:
        print(f"NAME locator check failed: {exc}")
        results["NAME locator finds both login fields"] = False

    try:
        heading, links = locate_by_tag_name(driver)
        heading_valid = validate_text(heading, "Welcome to the-internet", "main page heading")
        results["TAG_NAME locator finds heading and links"] = bool(heading and links)
        results["Main heading text assertion"] = heading_valid
    except (NoSuchElementException, TimeoutException, WebDriverException) as exc:
        print(f"TAG_NAME locator check failed: {exc}")
        results["TAG_NAME locator finds heading and links"] = False
        results["Main heading text assertion"] = False

    print("\n=== LAB SUMMARY ===")
    for name, passed in results.items():
        print(f"{'PASS' if passed else 'FAIL'} - {name}")
    passed_count = sum(results.values())
    print(f"Result: {passed_count}/{len(results)} checks passed")
    return passed_count == len(results)


def main():
    driver = None
    try:
        driver = setup_driver()
        print("Lab 4: Introduction to Web Element Identification")
        success = run_lab(driver)
        if not success:
            raise SystemExit(1)
    except WebDriverException as exc:
        print(f"Browser setup or automation failed: {exc}")
        raise SystemExit(1) from exc
    finally:
        if driver is not None:
            driver.quit()
            print("Browser closed.")


if __name__ == "__main__":
    main()
