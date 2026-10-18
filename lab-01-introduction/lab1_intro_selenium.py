from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,1000")
    return webdriver.Chrome(options=options)


def main():
    driver = create_driver()
    try:
        driver.get("https://www.example.com")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        heading = driver.find_element(By.TAG_NAME, "h1").text
        assert heading == "Example Domain", f"Unexpected heading: {heading}"
        screenshot = Path("lab1_result.png")
        driver.save_screenshot(str(screenshot))
        print(f"Page title: {driver.title}")
        print(f"Main heading: {heading}")
        print(f"Screenshot saved: {screenshot.resolve()}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
