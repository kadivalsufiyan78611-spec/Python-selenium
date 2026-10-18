from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def demonstrate_element_location():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://the-internet.herokuapp.com/")
        wait = WebDriverWait(driver, 10)
        heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        by_link_text = driver.find_element(By.LINK_TEXT, "A/B Testing")
        by_css = driver.find_element(By.CSS_SELECTOR, "a[href='/login']")
        by_xpath = driver.find_element(By.XPATH, "//a[@href='/dropdown']")
        print("Heading:", heading.text)
        print("Link text:", by_link_text.text)
        print("CSS selector result:", by_css.text)
        print("XPath result:", by_xpath.text)
    finally:
        driver.quit()


if __name__ == "__main__":
    demonstrate_element_location()
