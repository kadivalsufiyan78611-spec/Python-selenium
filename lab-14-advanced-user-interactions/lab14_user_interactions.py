import logging
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).resolve().parent
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.FileHandler(BASE_DIR / "user_interactions.log", encoding="utf-8"),
                               logging.StreamHandler()])
logger = logging.getLogger(__name__)


class AdvancedUserInteractions:
    def __init__(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1440,1000")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 12)
        self.actions = ActionChains(self.driver)

    def hover_menu(self):
        self.driver.get("https://demoqa.com/menu")
        item = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Main Item 2']")))
        self.actions.move_to_element(item).perform()
        submenu = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Sub Item']")))
        self.actions.move_to_element(submenu).perform()
        logger.info("Hover menu and submenu were displayed.")

    def drag_and_drop(self):
        self.driver.get("https://demoqa.com/droppable")
        source = self.wait.until(EC.visibility_of_element_located((By.ID, "draggable")))
        target = self.wait.until(EC.visibility_of_element_located((By.ID, "droppable")))
        self.actions.drag_and_drop(source, target).perform()
        self.wait.until(lambda driver: "Dropped!" in driver.find_element(By.ID, "droppable").text)
        logger.info("Drag-and-drop state verified.")

    def click_patterns(self):
        self.driver.get("https://demoqa.com/buttons")
        double_button = self.wait.until(EC.element_to_be_clickable((By.ID, "doubleClickBtn")))
        self.actions.double_click(double_button).perform()
        self.wait.until(EC.visibility_of_element_located((By.ID, "doubleClickMessage")))
        right_button = self.wait.until(EC.element_to_be_clickable((By.ID, "rightClickBtn")))
        self.actions.context_click(right_button).perform()
        self.wait.until(EC.visibility_of_element_located((By.ID, "rightClickMessage")))
        logger.info("Double-click and context-click messages verified.")

    def run(self):
        try:
            self.hover_menu()
            self.drag_and_drop()
            self.click_patterns()
        except (TimeoutException, WebDriverException):
            self.driver.save_screenshot(str(BASE_DIR / "interaction_failure.png"))
            logger.exception("Interaction scenario failed; screenshot saved.")
            raise
        finally:
            self.driver.quit()


if __name__ == "__main__":
    AdvancedUserInteractions().run()
