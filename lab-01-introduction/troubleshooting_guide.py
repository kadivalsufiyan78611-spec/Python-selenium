from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def safe_find_element(driver, by, value, description, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    except TimeoutException as exc:
        raise RuntimeError(f"Timed out while locating {description}: {value}") from exc


def demonstrate_best_practices():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://the-internet.herokuapp.com/")
        heading = safe_find_element(driver, By.TAG_NAME, "h1", "page heading")
        print("Page heading:", heading.text)
        try:
            driver.find_element(By.ID, "element-that-does-not-exist")
        except NoSuchElementException:
            print("Expected example: element was not found.")
    finally:
        driver.quit()


if __name__ == "__main__":
    demonstrate_best_practices()
