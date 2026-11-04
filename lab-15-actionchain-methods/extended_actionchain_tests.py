import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(filename="extended_actionchain.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", filemode="w")

class ExtendedActionChainTests:
    def __init__(self):
        options = Options()
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def test_keyboard_shortcut(self):
        page = Path("keyboard_test.html").resolve()
        page.write_text("<html><body><textarea id='source'>Sample keyboard text</textarea></body></html>", encoding="utf-8")
        self.driver.get(page.as_uri())
        source = self.wait.until(EC.visibility_of_element_located((By.ID, "source")))
        source.click()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()
        logging.info("Sent CTRL+A to source text area")
        print("CTRL+A shortcut sent to the source text area.")

    def test_hover_and_context_click(self):
        self.driver.get("https://demoqa.com/menu")
        menu = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Main Item 2']")))
        ActionChains(self.driver).move_to_element(menu).perform()
        ActionChains(self.driver).context_click(menu).send_keys(Keys.ESCAPE).perform()
        logging.info("Hover and context-click performed")

    def test_double_click(self):
        self.driver.get("https://demoqa.com/buttons")
        button = self.wait.until(EC.element_to_be_clickable((By.ID, "doubleClickBtn")))
        ActionChains(self.driver).double_click(button).perform()
        message = self.wait.until(EC.visibility_of_element_located((By.ID, "doubleClickMessage"))).text
        logging.info("Double-click result: %s", message)
        print("Double-click result:", message)

    def run(self):
        try:
            self.test_keyboard_shortcut()
            self.test_hover_and_context_click()
            self.test_double_click()
        except Exception:
            logging.exception("Extended ActionChain tests failed")
            raise
        finally:
            self.driver.quit()

if __name__ == "__main__":
    ExtendedActionChainTests().run()
