from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_assertion_tests():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.example.com")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )
        assert driver.title == "Example Domain", f"Unexpected title: {driver.title}"
        heading = driver.find_element(By.TAG_NAME, "h1")
        assert heading.text == "Example Domain", f"Unexpected heading: {heading.text}"
        paragraph = driver.find_element(By.CSS_SELECTOR, "p")
        assert "illustrative examples" in paragraph.text.lower()
        print("All page assertions passed.")
    finally:
        driver.quit()


if __name__ == "__main__":
    run_assertion_tests()
