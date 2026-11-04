import logging
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).resolve().parent
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler(BASE_DIR / "intelligent_sync.log", encoding="utf-8"),
                               logging.StreamHandler()])
logger = logging.getLogger(__name__)


class IntelligentSyncAutomation:
    def __init__(self, timeout=10):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, timeout)

    def wait_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def wait_invisible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    @staticmethod
    def retry(action, attempts=3, delay=1):
        last_error = None
        for attempt in range(1, attempts + 1):
            try:
                return action()
            except (TimeoutException, WebDriverException) as exc:
                last_error = exc
                logger.warning("Attempt %d/%d failed: %s", attempt, attempts, exc.__class__.__name__)
                if attempt < attempts:
                    time.sleep(delay)
        raise last_error

    def test_dynamic_controls(self):
        self.driver.get("https://the-internet.herokuapp.com/dynamic_controls")
        checkbox = (By.CSS_SELECTOR, "#checkbox input")
        button = (By.CSS_SELECTOR, "#checkbox button")
        self.wait_visible(checkbox)
        self.retry(lambda: self.wait_clickable(button).click())
        self.wait_invisible(checkbox)
        add_button = self.wait_clickable(button)
        if add_button.text.strip() != "Add":
            raise AssertionError("Expected Add button after checkbox removal")
        self.retry(lambda: self.wait_clickable(button).click())
        self.wait_visible(checkbox)
        logger.info("Remove/Add control verified.")

    def test_enable_disable(self):
        input_locator = (By.CSS_SELECTOR, "#input-example input")
        button_locator = (By.CSS_SELECTOR, "#input-example button")
        self.wait_visible(input_locator)
        self.retry(lambda: self.wait_clickable(button_locator).click())
        self.wait.until(lambda driver: driver.find_element(*input_locator).is_enabled())
        field = self.driver.find_element(*input_locator)
        field.clear()
        field.send_keys("Intelligent synchronization")
        self.retry(lambda: self.wait_clickable(button_locator).click())
        self.wait.until(lambda driver: not driver.find_element(*input_locator).is_enabled())
        logger.info("Enable/Disable control verified.")

    def run(self):
        try:
            self.test_dynamic_controls()
            self.test_enable_disable()
        finally:
            self.driver.quit()


if __name__ == "__main__":
    IntelligentSyncAutomation().run()
