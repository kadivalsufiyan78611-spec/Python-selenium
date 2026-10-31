import logging
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / "artifacts"
UPLOAD_FILE = BASE / "test_upload.txt"


class WebAutomationChallenges:
    def __init__(self, headless=True, timeout=15):
        OUTPUT.mkdir(exist_ok=True)
        self.logger = logging.getLogger("lab6")
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handlers = [
            logging.FileHandler(OUTPUT / f"automation_{datetime.now():%Y%m%d_%H%M%S}.log", encoding="utf-8"),
            logging.StreamHandler(),
        ]
        for handler in handlers:
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.driver = None
        self.wait = None
        self.headless = headless
        self.timeout = timeout

    def setup_driver(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        try:
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, self.timeout)
            self.logger.info("Chrome WebDriver initialized")
            return True
        except WebDriverException:
            self.logger.exception("Driver initialization failed")
            return False

    def screenshot(self, label):
        if self.driver:
            path = OUTPUT / f"{label}_{datetime.now():%Y%m%d_%H%M%S}.png"
            try:
                self.driver.save_screenshot(str(path))
                self.logger.info("Screenshot saved: %s", path)
            except WebDriverException:
                self.logger.exception("Screenshot capture failed")

    def handle_dynamic_loading(self):
        try:
            self.driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))).click()
            self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
            text = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4"))).text.strip()
            if text != "Hello World!":
                raise AssertionError(f"Unexpected dynamic text: {text!r}")
            self.logger.info("Dynamic loading passed")
            return True
        except (TimeoutException, AssertionError, WebDriverException):
            self.logger.exception("Dynamic loading failed")
            self.screenshot("dynamic_loading_failure")
            return False

    def handle_file_upload(self):
        try:
            if not UPLOAD_FILE.is_file():
                raise FileNotFoundError(f"Missing upload fixture: {UPLOAD_FILE}")
            self.driver.get("https://the-internet.herokuapp.com/upload")
            self.wait.until(EC.presence_of_element_located((By.ID, "file-upload"))).send_keys(str(UPLOAD_FILE.resolve()))
            self.driver.find_element(By.ID, "file-submit").click()
            heading = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
            filename = self.wait.until(EC.visibility_of_element_located((By.ID, "uploaded-files"))).text.strip()
            if "File Uploaded!" not in heading or UPLOAD_FILE.name not in filename:
                raise AssertionError(f"Upload verification failed: {heading!r}, {filename!r}")
            self.logger.info("File upload passed: %s", filename)
            return True
        except (TimeoutException, AssertionError, FileNotFoundError, WebDriverException):
            self.logger.exception("File upload failed")
            self.screenshot("file_upload_failure")
            return False

    def handle_javascript_dropdown(self):
        try:
            self.driver.get("https://the-internet.herokuapp.com/dropdown")
            dropdown = self.wait.until(EC.presence_of_element_located((By.ID, "dropdown")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
            self.driver.execute_script("arguments[0].value='1'; arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", dropdown)
            selected = Select(dropdown).first_selected_option.get_attribute("value")
            if selected != "1":
                raise AssertionError(f"Expected option 1, got {selected!r}")
            self.logger.info("JavaScript dropdown interaction passed")
            return True
        except (TimeoutException, AssertionError, WebDriverException):
            self.logger.exception("JavaScript dropdown interaction failed")
            self.screenshot("dropdown_failure")
            return False

    def demonstrate_javascript_techniques(self):
        try:
            self.driver.get("https://the-internet.herokuapp.com/checkboxes")
            elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='checkbox']")))
            for index, element in enumerate(elements, 1):
                visible = self.driver.execute_script("const r=arguments[0].getBoundingClientRect(); return r.width>0 && r.height>0;", element)
                if visible and not element.is_selected():
                    self.driver.execute_script("arguments[0].click();", element)
                self.logger.info("Checkbox %s selected=%s visible=%s", index, element.is_selected(), visible)
            return all(element.is_selected() for element in elements)
        except WebDriverException:
            self.logger.exception("JavaScript checkbox demonstration failed")
            self.screenshot("javascript_failure")
            return False

    def test_error_scenarios(self):
        checks = []
        try:
            self.driver.get("https://the-internet.herokuapp.com/")
            try:
                self.wait.until(EC.presence_of_element_located((By.ID, "missing-lab6-element")))
            except TimeoutException:
                self.logger.info("Expected missing-element timeout captured")
                self.screenshot("expected_missing_element")
                checks.append(True)
            self.driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
            try:
                self.driver.find_element(By.CSS_SELECTOR, "#finish h4").click()
            except (NoSuchElementException, ElementNotInteractableException):
                self.logger.info("Expected hidden-element interaction issue captured")
                self.screenshot("expected_hidden_element")
                checks.append(True)
            return len(checks) == 2 and all(checks)
        except WebDriverException:
            self.logger.exception("Error scenario failed")
            self.screenshot("error_scenarios_failure")
            return False

    def generate_test_report(self, results):
        total = len(results)
        passed = sum(results.values())
        report = OUTPUT / f"test_report_{datetime.now():%Y%m%d_%H%M%S}.txt"
        lines = ["Lab 6 - Web Element Identification Challenges", f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}", ""]
        lines.extend(f"{name}: {'PASSED' if result else 'FAILED'}" for name, result in results.items())
        lines.extend(["", f"Total: {total}", f"Passed: {passed}", f"Failed: {total-passed}", f"Success rate: {passed/total*100 if total else 0:.1f}%"])
        report.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.logger.info("Report saved: %s", report)

    def cleanup(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logger.info("WebDriver closed")


def main():
    automation = WebAutomationChallenges()
    results = {}
    try:
        if not automation.setup_driver():
            raise RuntimeError("Chrome WebDriver could not be initialized")
        tests = [
            ("Dynamic loading", automation.handle_dynamic_loading),
            ("File upload", automation.handle_file_upload),
            ("JavaScript dropdown", automation.handle_javascript_dropdown),
            ("JavaScript checkbox interaction", automation.demonstrate_javascript_techniques),
            ("Expected error scenarios", automation.test_error_scenarios),
        ]
        for name, test in tests:
            print(f"\nRunning: {name}")
            results[name] = test()
            print(f"Result: {'PASSED' if results[name] else 'FAILED'}")
        automation.generate_test_report(results)
        return 0 if all(results.values()) else 1
    finally:
        automation.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
